# PythonTestFramework
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
  - Be able to validate how long the product take to:
    - "time_to_request": Time between page start or page action to when the request of interest fired
    - "request_start_time": Time when request started
    - "response_start_time": Time when response started
    - "response_end_time": Time when response ended
    - "request_total_time": Time between page start or page action tp response end time




Framework is under development
