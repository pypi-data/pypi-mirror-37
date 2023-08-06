
"Events Module\n\nThis module mirrors the Events API. It allows you to get, post, update, and delete events.\n\nhttps://doc.cognitedata.com/0.5/#Cognite-API-Events\n"
import json
from cognite import _constants, _utils, config
from cognite.v05.dto import EventListResponse, EventResponse


def get_event(event_id, **kwargs):
    "Returns a EventResponse containing an event matching the id.\n\n    Args:\n        event_id (int):         The event id.\n\n    Keyword Arguments:\n        api_key (str):          Your api-key.\n\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.EventResponse: A data object containing the requested event.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.5/projects/{}/events/{}".format(project, event_id)
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    res = _utils.get_request(url, headers=headers, cookies=config.get_cookies())
    return EventResponse(res.json())


def get_events(type=None, sub_type=None, asset_id=None, **kwargs):
    "Returns an EventListReponse object containing events matching the query.\n\n    Args:\n        type (str):             Type (class) of event, e.g. 'failure'.\n        sub_type (str):         Sub-type of event, e.g. 'electrical'.\n        asset_id (str):         Return events associated with this assetId.\n    Keyword Arguments:\n        sort (str):             Sort descending or ascending. Default 'ASC'.\n        cursor (str):           Cursor to use for paging through results.\n        limit (int):            Return up to this many results. Maximum is 10000. Default is 25.\n        has_description (bool): Return only events that have a textual description. Default null. False gives only\n                                those without description.\n        min_start_time (string): Only return events from after this time.\n        max_start_time (string): Only return events form before this time.\n        api_key (str):          Your api-key.\n        project (str):          Project name.\n        autopaging (bool):      Whether or not to automatically page through results. If set to true, limit will be\n                                disregarded. Defaults to False.\n\n    Returns:\n        v05.dto.EventListResponse: A data object containing the requested event.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.5/projects/{}/events".format(project)
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    if asset_id:
        params = {
            "assetId": asset_id,
            "sort": kwargs.get("sort"),
            "cursor": kwargs.get("cursor"),
            "limit": (kwargs.get("limit", 25) if (not kwargs.get("autopaging")) else _constants.LIMIT_AGG),
        }
    else:
        params = {
            "type": type,
            "subtype": sub_type,
            "assetId": asset_id,
            "sort": kwargs.get("sort"),
            "cursor": kwargs.get("cursor"),
            "limit": (kwargs.get("limit", 25) if (not kwargs.get("autopaging")) else _constants.LIMIT_AGG),
            "hasDescription": kwargs.get("has_description"),
            "minStartTime": kwargs.get("min_start_time"),
            "maxStartTime": kwargs.get("max_start_time"),
        }
    res = _utils.get_request(url, headers=headers, params=params, cookies=config.get_cookies())
    events = []
    events.extend(res.json()["data"]["items"])
    next_cursor = res.json()["data"].get("nextCursor")
    while next_cursor and kwargs.get("autopaging"):
        params["cursor"] = next_cursor
        res = _utils.get_request(url=url, headers=headers, params=params, cookies=config.get_cookies())
        events.extend(res.json()["data"]["items"])
        next_cursor = res.json()["data"].get("nextCursor")
    return EventListResponse(
        {
            "data": {
                "nextCursor": next_cursor,
                "previousCursor": res.json()["data"].get("previousCursor"),
                "items": events,
            }
        }
    )


def post_events(events, **kwargs):
    "Adds a list of events and returns an EventListResponse object containing created events.\n\n    Args:\n        events (List[v05.dto.Event]):    List of events to create.\n\n    Keyword Args:\n        api_key (str):          Your api-key.\n        project (str):          Project name.\n\n    Returns:\n        v05.dto.EventListResponse\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.5/projects/{}/events".format(project)
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    body = {"items": [event.__dict__ for event in events]}
    res = _utils.post_request(url, body=body, headers=headers)
    return EventListResponse(res.json())


def delete_events(event_ids, **kwargs):
    "Deletes a list of events.\n\n    Args:\n        event_ids (List[int]):    List of ids of events to delete.\n\n    Keyword Args:\n        api_key (str):          Your api-key.\n        project (str):          Project name.\n\n    Returns:\n        An empty response.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.5/projects/{}/events/delete".format(project)
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    body = {"items": event_ids}
    res = _utils.post_request(url, body=body, headers=headers)
    return res.json()


def search_for_events(
    description=None,
    type=None,
    subtype=None,
    min_start_time=None,
    max_start_time=None,
    min_end_time=None,
    max_end_time=None,
    min_created_time=None,
    max_created_time=None,
    min_last_updated_time=None,
    max_last_updated_time=None,
    metadata=None,
    asset_ids=None,
    asset_subtrees=None,
    **kwargs
):
    'Search for events.\n\n        Args:\n            description str:   Prefix and fuzzy search on description.\n\n        Keyword Args:\n            api_key (str):          Your api-key.\n            project (str):          Project name.\n            type (str):             Filter on type (case-sensitive).\n            subtype (str):          Filter on subtype (case-sensitive).\n            min_start_time (str):   Filter out events with startTime before this. Format is milliseconds since epoch.\n            max_start_time (str):   Filter out events with startTime after this. Format is milliseconds since epoch.\n            min_end_time (str):     Filter out events with endTime before this. Format is milliseconds since epoch.\n            max_end_time (str):     Filter out events with endTime after this. Format is milliseconds since epoch.\n            min_created_time(str):  Filter out events with createdTime before this. Format is milliseconds since epoch.\n            max_created_time (str): Filter out events with createdTime after this. Format is milliseconds since epoch.\n            min_last_updated_time(str):  Filter out events with lastUpdatedtime before this. Format is milliseconds since epoch.\n            max_last_updated_time(str): Filter out events with lastUpdatedtime after this. Format is milliseconds since epoch.\n            metadata (dict):        Filter out events that do not match these metadata fields and values (case-sensitive).\n                                    Format is {"key1":"value1","key2":"value2"}.\n            asset_ids (List[int]):  Filter out events that are not linked to any of these assets. Format is [12,345,6,7890].\n            asset_subtrees (List[int]): Filter out events that are not linked to assets in the subtree rooted at these assets.\n                                        Format is [12,345,6,7890].\n\n        Keyword Args:\n            sort (str):             Field to be sorted.\n            dir (str):              Sort direction (desc or asc)\n            limit (int):            Return up to this many results. Max is 1000, default is 25.\n            offset (int):           Offset from the first result. Sum of limit and offset must not exceed 1000. Default is 0.\n        Returns:\n            v05.dto.EventListResponse.\n        '
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.5/projects/{}/events/search".format(project)
    headers = {"api-key": api_key, "content-type": "application/json", "accept": "application/json"}
    params = {
        "description": description,
        "type": type,
        "subtype": subtype,
        "minStartTime": min_start_time,
        "maxStartTime": max_start_time,
        "minEndTime": min_end_time,
        "maxEndTime": max_end_time,
        "minCreatedTime": min_created_time,
        "maxCreatedTime": max_created_time,
        "minLastUpdatedTime": min_last_updated_time,
        "maxLastUpdatedTime": max_last_updated_time,
        "metadata": json.dumps(metadata),
        "assetIds": str((asset_ids or [])),
        "assetSubtrees": asset_subtrees,
        "sort": kwargs.get("sort"),
        "dir": kwargs.get("dir"),
        "limit": kwargs.get("limit", 1000),
        "offset": kwargs.get("offset"),
    }
    res = _utils.get_request(url, headers=headers, params=params)
    return EventListResponse(res.json())
