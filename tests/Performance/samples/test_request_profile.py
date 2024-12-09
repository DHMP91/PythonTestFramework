import pytest
from pandas import DataFrame
from libs.Performance.browser_performance import RequestProfiling, NetworkType
from hamcrest import assert_that, less_than

from libs.hamcrest_matcher import is_within_range


@pytest.mark.PERFORMANCE
@pytest.mark.CHROMIUM
def test_profile_get_repository_request(context):
    page = context.new_page()
    url = "https://github.com/DHMP91?tab=repositories"

    def page_action():
        page.goto(url)
        page.reload()

    match_request = lambda request: request.url == url and request.method == "GET"

    rb = RequestProfiling(page)
    stats: DataFrame = rb.run(page_action, match_request, emulate_network=NetworkType.MOBILE_5G)
    assert_that(stats["request_total_time"].median(), is_within_range(50, 200))


