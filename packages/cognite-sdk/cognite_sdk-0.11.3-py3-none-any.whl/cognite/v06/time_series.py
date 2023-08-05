
"Timeseries Module\n\nThis module mirrors the Timeseries API. It allows you to fetch data from the api and output it in various formats.\n\nhttps://doc.cognitedata.com/0.6/#Cognite-API-Time-series\n"
from cognite import _utils, config
from cognite.v05.dto import TimeSeriesResponse


def get_time_series_by_id(id, include_metadata=False, **kwargs):
    "Returns a TimeseriesResponse object containing the requested timeseries.\n\n    Args:\n        id (int):           ID of timeseries to look up\n\n        include_metadata (bool):    Decide if the metadata field should be returned or not. Defaults to False.\n\n    Keyword Arguments:\n        api_key (str):          Your api-key.\n\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.TimeSeriesResponse: A data object containing the requested timeseries.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/timeseries/{}".format(project, id)
    headers = {"api-key": api_key, "accept": "application/json"}
    params = {"includeMetadata": include_metadata}
    res = _utils.get_request(url=url, headers=headers, params=params, cookies=config.get_cookies())
    return TimeSeriesResponse(res.json())


def get_multiple_time_series_by_id(ids, include_metadata=False, **kwargs):
    "Returns a TimeseriesResponse object containing the requested timeseries.\n\n    Args:\n        ids (List[int]):           IDs of timeseries to look up\n\n    Keyword Arguments:\n        api_key (str):          Your api-key.\n\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.TimeSeriesResponse: A data object containing the requested timeseries with several getter methods with different\n        output formats.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/timeseries/byids".format(project)
    headers = {"api-key": api_key, "accept": "application/json", "content-type": "application/json"}
    body = {"items": ids}
    params = {"includeMetadata": include_metadata}
    res = _utils.post_request(url=url, body=body, params=params, headers=headers, cookies=config.get_cookies())
    return TimeSeriesResponse(res.json())
