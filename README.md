# PythonTestFramework (Currently under development)
Curated Framework with mix of custom and 3rd party testing library to achieve UI, API and Performance testing needs. Focus is on flexibility and extensibility.


# Overview library and custom features of this framework
Library:
- Playwright https://github.com/microsoft/playwright-python
- Playwright pytest plugin https://github.com/microsoft/playwright-pytest



Custom features:
- Page object model implementation with Playwright https://github.com/DHMP91/PlayPOM/
  - samples: tests/UI/sample/test_github.py, tests/UI/sample/test_google.py
- Request level profiling:
  - Every product have specific request(s) that needs special validation points
    - samples: tests/Performance/samples/test_request_profile.py
  - Be able to validate product timing at the browser's network request level:
    - "time_to_request": Time between page start or page action to when the request of interest fired
    - "request_start_time": Time when request started
    - "response_start_time": Time when response started
    - "response_end_time": Time when response ended
    - "request_total_time": Time between page start or page action tp response end time


# Q & A:
**Why is "time_to_request" an important metric?**

A: It is crucial to understand how a browser loads a page and when it sends a request to the server for information. Often, test engineers focus solely on how quickly a request is executed, overlooking the time the browser takes to load resources, process the page, and handle other tasks before the request is even initiated. In some cases, several seconds may pass before a request is fired, even if the request itself is fast. 

Having automated test that monitor the timing is important for product user perceived performance.


