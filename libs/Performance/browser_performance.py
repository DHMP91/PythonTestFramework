import csv
import tempfile
import time
from enum import Enum

import pandas
from typing import Callable

from pandas import DataFrame
from playwright.sync_api import Page, Request, BrowserType

class NetworkType(Enum):
    MOBILE_5G = 1


NETWORK_SETTINGS = {
    NetworkType.MOBILE_5G: {
        "offline": False,
        "downloadThroughput": 50000000 / 8,  # 50 Mbps (convert to bytes per second)
        "uploadThroughput": 10000000 / 8,    # 10 Mbps (convert to bytes per second)
        "latency": 20                        # 20ms latency
    }
}


class RequestProfiling(object):
    __stats = {
        "test_start_time": 0.00,
        "time_to_request": 0.00,
        "request_start_time": 0.00,
        "response_start_time": 0.00,
        "response_end_time": 0.00,
        "request_total_time": 0.00,
    }

    def __init__(self, page: Page):
        self.page: Page = page

    def run(self, perform_action: Callable, request_matcher: Callable[[Request], bool], sample_size = 10, sampling_interval = 1000, emulate_network: NetworkType = None) -> DataFrame:
        """
        :param perform_action:  Function call to trigger the request of interest.
                                Timer start function returns.
                                Function can return a time stamp (seconds) for more precise start time.
        :param request_matcher: matcher to find request of interest.
        :param sample_size: Default 10. Run the perform_action N amount of times
        :param sampling_interval: Default 1. Sleep time between sampling in milliseconds
        :param emulate_network: Default None: Set the browser to an emulated network speed. Chromium only
        :return: dictionary of statistic in milliseconds
                {
                    "test_start_time": float, # When the test timer started
                    "time_to_request": float, # Time between timer started to request fired
                    "request_start_time": float, # Time when request started
                    "response_start_time": float, # Time when response started
                    "response_end_time": float, # Time when response ended
                    "request_total_time": float, # Time between test started and response end time
                }
        """

        if emulate_network and self.page.context.browser.browser_type.name.lower() == "chromium":
            network_conditions = NETWORK_SETTINGS[emulate_network]
            session = None
            try:
                session = self.page.context.new_cdp_session(self.page)
                session.send("Network.emulateNetworkConditions", network_conditions)
            finally:
                if session:
                    session.detach()


        keys = self.__stats.keys()
        tmp_file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False)
        with open(tmp_file.name, "w", newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            for i in range(0, sample_size):
                stats = next(self.__sample(perform_action, request_matcher))
                writer.writerow(stats)
                time.sleep(sampling_interval / 1000)

        chunks = pandas.read_csv(tmp_file.name, chunksize=100000)

        descriptive_stats = []
        for chunk in chunks:
            descriptive_stats.append(chunk.describe())

        final_stats = pandas.concat(descriptive_stats).describe()

        return final_stats


    def __sample(self, perform_action: Callable, request_matcher: Callable[[Request], bool]):
        while True:
            with self.page.expect_request(lambda request: request_matcher(request)) as request_info:
                now = time.time()
                func_time = perform_action()
                if func_time:
                    now = func_time

            request_data = request_info.value
            request_resource_timing = request_data.timing
            sample_stat = self.__stats
            sample_stat["test_start_time"] = now * 1000
            time_to_request = request_resource_timing["startTime"] - sample_stat["test_start_time"]
            sample_stat["time_to_request"] = time_to_request
            sample_stat["request_start_time"] = request_resource_timing["startTime"]
            sample_stat["response_start_time"] = request_resource_timing["startTime"] + request_resource_timing[
                "responseStart"]
            sample_stat["response_end_time"] = request_resource_timing["startTime"] + request_resource_timing[
                "responseEnd"]
            sample_stat["request_total_time"] = sample_stat["response_end_time"] - sample_stat["test_start_time"]

            yield sample_stat








