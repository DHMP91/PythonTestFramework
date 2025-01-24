# Global conftest for all UI/PERFORMANCE/API/ related fixtures
from __future__ import annotations

import datetime
import hashlib
import inspect
from typing import Union

import pytest
import logging
import httpx

from httpx import ConnectError
from libs.API.pytad.client.pytad_api_client import AuthenticatedClient
from libs.API.pytad.client.pytad_api_client.api.health import get_health
from libs.API.pytad.client.pytad_api_client.api.testcases import (
    create_test_case,
    create_test_run,
    get_test_run,
    update_test_run,

)
from libs.API.pytad.client.pytad_api_client.models import StatusEnum, TestRun
from libs.API.pytad.client.pytad_api_client.models.test_case import TestCase
from libs.API.pytad.client.pytad_api_client.models.new_test_case import NewTestCase
from libs.API.pytad.client.pytad_api_client.models.new_test_run import NewTestRun
from libs.API.pytad.client.pytad_api_client.types import Response

LOGGER = logging.getLogger(__name__)


class PyTADInvalidTokenException(Exception):
    pass

@pytest.fixture(autouse=True, scope="session")
def pytad_configured(variables) -> bool:
    # Check if pytad is enabled from variables common.yaml
    if 'pytad' in variables and variables['pytad']['enable']:
        url = variables['pytad']['base_url']
        token: str = variables['pytad']['api_key']
        if token == "":
            raise PyTADInvalidTokenException("API Key is empty")

        # Make request to PyTAD health endpoint to server access and token
        client = AuthenticatedClient(base_url=url, prefix="Token", token=token)
        try:
            response = get_health.sync_detailed(client=client)
            if httpx.codes.is_success(response.status_code):
                return True
            elif response.status_code == httpx.codes.UNAUTHORIZED :
                LOGGER.error(f"PYTAD Unauthorized. reason={str(response.content)}")
            else:
                LOGGER.error(f"PYTAD configuration test failed. {response.status_code} reason={response.content}")
        except ConnectError as e:
            LOGGER.error(f"PYTAD Could not connect to PYTAD server on {url}. Is it up and running?")
    return False

@pytest.fixture(scope="session")
def pytad_client(variables, pytad_configured) -> AuthenticatedClient:
    # Session based authenticated client for PYTAD
    if pytad_configured:
        url = variables['pytad']['base_url']
        token: str = variables['pytad']['api_key']
        return AuthenticatedClient(base_url=url, prefix="Token", token=token)

@pytest.fixture(autouse=True)
def pytad_test_setup_teardown(request, pytad_configured, pytad_client) -> int:
    if pytad_configured:
        # Setup: create/reuse test case and create a new test run for test
        test_function = request.node.function
        code = __get_function_body(test_function)
        code_hash = hashlib.md5(code.encode()).hexdigest()
        test_id = __create_test_case(pytad_client, request, code, code_hash)
        test_run_id = None
        if test_id:
            test_run_name = request.node.name
            test_run_id = __create_test_run(pytad_client, test_id, test_run_name, code_hash)
        yield test_run_id
        # Teardown: update test if a test run exists
        if test_run_id:
            __update_test(pytad_client, request, test_run_id)
    else:
        LOGGER.debug("PYTAD is not configured")
        yield

def __create_test_case(client: AuthenticatedClient, request, code: str, code_hash: str) -> Union[int, None]:
    """
    Register/Create a new test case on PyTAD
    :param client: httpx authenticated client for PYTAD
    :param request: pytest request fixture
    :return:
    """

    # Extract test information from pytest request fixture
    module = request.node.parent.nodeid
    test_name = request.node.originalname
    test_relative_path = f"{module}::{test_name}"
    test_internal_id = next(
        (mark.kwargs['id'] for mark in request.node.iter_markers() if mark.name == "test_id" and "id" in mark.kwargs),
        None
    )

    # New test case object
    new_test_case = NewTestCase(
        id=0,
        name=test_name,
        relative_path=test_relative_path,
        create_date=datetime.datetime.now(),
        code_hash = code_hash,
        code = code,
        internal_id = test_internal_id
    )

    # Send request to pytad to create test case
    create_response: Response[TestCase] = (
        create_test_case
        .sync_detailed(client=client,body=new_test_case)
    )
    if httpx.codes.is_success(create_response.status_code):
        test_id = create_response.parsed.id
        if create_response.status_code == httpx.codes.OK:
            LOGGER.debug("PYTAD test case already exists. Re-using test case {test}")
        return test_id
    else:
        LOGGER.error(f"PYTAD test case creation failed. {create_response.status_code} reason={create_response.content}")
    return None

def __create_test_run(client: AuthenticatedClient, test_id: int, test_run_name: str, code_hash: str) -> int:
    """
    Create new test run for test case.
    :param test_id: ID of testcase associated with this test run
    :param test_run_name: name for this test run
    :param client: httpx authenticated client for PYTAD
    :return:
        int: test run id
    """
    body = NewTestRun(
        name=test_run_name,
        status=StatusEnum.INPROGRESS,
        start_time=datetime.datetime.now(),
        code_hash=code_hash
    )
    response: Response[TestRun] = create_test_run.sync_detailed(id=test_id, client=client, body=body)
    if httpx.codes.is_success(response.status_code):
        return response.parsed.id
    else:
        LOGGER.error(f"PYTAD test run creation failed. {response.status_code} reason={response.content}")

def __update_test(client: AuthenticatedClient, request, test_run_id: int):
    """
    Update the test run with status, endtime, marks

    :param test_run_id: id of the test run to update
    :param request: pytest SubRequest fixture
    :param client: httpx authenticated client for PYTAD

    :return: None
    """
    try:
        status: str = request.node.rep_call.outcome # Get the test result from outcome
        status = StatusEnum(status.upper()) # Map to Status
        xfail = hasattr(request.node.rep_call, 'wasxfail') # Check if the pass or failure is unexpected or expected
        if status == StatusEnum.FAILED and xfail:
            status = StatusEnum.XFAILED # Set as expected failure
        elif status == StatusEnum.PASSED and xfail:
            status = StatusEnum.XPASSED # Set as unexpected failure
    except Exception as e:
        LOGGER.debug(f"PYTAD Could not determine status for test run {test_run_id}. {e}")
        status = StatusEnum.UNKNOWN

    # Get test run instance from pytad and set updated infomation
    get_response: Response[TestRun] = get_test_run.sync_detailed(test_run_id, client=client)
    test_run = get_response.parsed
    test_run.status = status
    test_run.end_time = datetime.datetime.now()
    marks = [mark.name for mark in request.node.iter_markers()]
    test_run.marks = ",".join(marks)

    # Send request to update test run
    update_response: Response[TestRun] = (
        update_test_run
        .sync_detailed(test_run_id, client=client, body=test_run)
    )
    if not httpx.codes.is_success(update_response.status_code):
        LOGGER.error(
            f"PYTAD Could update test run {test_run_id}. "
            f"{update_response.status_code} reason={update_response.content}"
        )

def __get_function_body(function) -> Union[str, None]:
    """
    Extract the body of the function as a string
    :param function: the function object
    :return: the body of the function (str)
    """
    try:
        source_lines, start_line = inspect.getsourcelines(function)
        start_index = next(i for i in range(len(source_lines)) if source_lines[i].lstrip().startswith("def test"))
        if start_index is None:
            LOGGER.error(f"PYTAD Error extracting function body. Cannot find function starting line")
            return None

        function_body_lines = source_lines[start_index+1:]
        return "".join(function_body_lines)

    except Exception as e:
        LOGGER.error(f"PYTAD Error extracting function body: {e}")
        return None
