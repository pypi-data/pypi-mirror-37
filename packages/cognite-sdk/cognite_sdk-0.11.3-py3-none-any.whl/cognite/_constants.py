
"Constants\n\nThis module contains constants used in the Cognite Python SDK.\n\nThis module is protected and should not used by end-users.\n\nAttributes:\n    BASE_URL (str):    Base url for Cognite API. Should have correct version number.\n    LIMIT (int):       Limit on how many datapoints should be returned from the API when fetching data using the\n                        timeseries module.\n    RETRY_LIMIT (int): Number of retries to perform if a request to the API should fail.\n"
import os

BASE_URL = "https://api.cognitedata.com"
LIMIT = 100000
LIMIT_AGG = 10000
RETRY_LIMIT = 0
NUM_OF_WORKERS = 10
TIMESERIES = "timeSeries"
AGGREGATES = "aggregates"
GRANULARITY = "granularity"
START = "start"
END = "end"
MISSING_DATA_STRATEGY = "missingDataStrategy"
LABEL = "label"
