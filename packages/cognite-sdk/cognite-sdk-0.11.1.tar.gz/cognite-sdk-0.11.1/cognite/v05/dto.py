
"Data Objects\n\nThis module contains data objects used to represent the data returned from the API. These objects have at least\nthe following output formats:\n\n    * to_pandas():    Returns pandas dataframe\n    * to_ndarray():   Numpy array\n    * to_json():      Json format\n"
import abc
import json
from copy import deepcopy
import pandas as pd
import six
from cognite import _utils


@six.add_metaclass(abc.ABCMeta)
class CogniteDataObject:
    "Abstract Cognite Data Object\n\n    This abstract class provides a skeleton for all data objects in this module. All data objects should inherit\n    this class.\n    "

    def __init__(self, internal_representation):
        self.internal_representation = internal_representation

    @abc.abstractmethod
    def to_pandas(self):
        "Returns data as a pandas dataframe"
        pass

    @abc.abstractmethod
    def to_json(self):
        "Returns data as a json object"
        pass

    def to_ndarray(self):
        "Returns data as a numpy array"
        return self.to_pandas().values

    def next_cursor(self):
        "Returns next cursor to use for paging through results"
        if self.internal_representation.get("data"):
            return self.internal_representation.get("data").get("nextCursor")

    def previous_cursor(self):
        "Returns previous cursor"
        if self.internal_representation.get("data"):
            return self.internal_representation.get("data").get("previousCursor")


class RawResponse(CogniteDataObject):
    "Raw Response Object."

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        return pd.DataFrame(self.internal_representation["data"]["items"])


class RawRow(object):
    "DTO for a row in a raw database.\n\n    The Raw API is a simple key/value-store. Each row in a table in a raw database consists of a\n    unique row key and a set of columns.\n\n    Attributes:\n        key (str):      Unique key for the row.\n\n        columns (int):  A key/value-map consisting of the values in the row.\n    "

    def __init__(self, key, columns):
        self.key = key
        self.columns = columns

    def __repr__(self):
        return json.dumps(self.repr_json())

    def repr_json(self):
        return self.__dict__


class TagMatchingResponse(CogniteDataObject):
    "Tag Matching Response Object.\n\n    In addition to the standard output formats this data object also has a to_list() method which returns a list of\n    names of the tag matches.\n    "

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        matches = []
        for tag in self.internal_representation["data"]["items"]:
            for match in tag["matches"]:
                matches.append(
                    {
                        "tag": tag["tagId"],
                        "match": match["tagId"],
                        "score": match["score"],
                        "platform": match["platform"],
                    }
                )
        if matches:
            return pd.DataFrame(matches)[["tag", "match", "platform", "score"]]
        return pd.DataFrame()

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"]

    def to_list(self, first_matches_only=True):
        "Returns a list representation of the matches.\n\n        Args:\n            first_matches_only (bool):      Boolean determining whether or not to return only the top match for each\n                                            tag.\n\n        Returns:\n            list: list of matched tags.\n        "
        if self.to_pandas().empty:
            return []
        if first_matches_only:
            return self.to_pandas().sort_values(["score", "match"]).groupby(["tag"]).first()["match"].tolist()
        return self.to_pandas().sort_values(["score", "match"])["match"].tolist()


class DatapointsQuery:
    "Data Query Object for Datapoints.\n\n    Attributes:\n        name (str):           Unique name of the time series.\n        aggregates (list):          The aggregate functions to be returned. Use default if null. An empty string must\n                                    be sent to get raw data if the default is a set of aggregate functions.\n        granularity (str):          The granularity size and granularity of the aggregates.\n        start (str, int, datetime): Get datapoints after this time. Format is N[timeunit]-ago where timeunit is w,d,h,m,s.\n                                    Example: '2d-ago' will get everything that is up to 2 days old. Can also send time in\n                                    ms since epoch or as a datetime object.\n        end (str, int, datetime):   Get datapoints up to this time. The format is the same as for start.\n    "

    def __init__(self, name, aggregates=None, granularity=None, start=None, end=None, limit=None):
        self.name = name
        self.aggregates = ",".join(aggregates) if (aggregates is not None) else None
        self.granularity = granularity
        (self.start, self.end) = _utils.interval_to_ms(start, end)
        if not start:
            self.start = None
        if not end:
            self.end = None
        self.limit = limit


class DatapointsResponse(CogniteDataObject):
    "Datapoints Response Object."

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"][0]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        return pd.DataFrame(self.internal_representation["data"]["items"][0]["datapoints"])


class DatapointsResponseIterator:
    "Iterator for Datapoints Response Objects."

    def __init__(self, datapoints_objects):
        self.datapoints_objects = datapoints_objects
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter > (len(self.datapoints_objects) - 1):
            raise StopIteration
        else:
            self.counter += 1
            return self.datapoints_objects[(self.counter - 1)]


class DatapointDepth(object):
    "Data transfer object for Depth datapoints.\n\n       Attributes:\n           depth (double): The depth (in m) of the datapoint \n           value (string):     The data value, Can be string or numeric depending on the metric.\n       "

    def __init__(self, depth, value):
        self.depth = depth
        self.value = value


class Datapoint(object):
    "Data transfer object for datapoints.\n\n    Attributes:\n        timestamp (int, datetime): The data timestamp in milliseconds since the epoch (Jan 1, 1970) or as a datetime object.\n        value (string):     The data value, Can be string or numeric depending on the metric.\n    "

    def __init__(self, timestamp, value):
        self.timestamp = timestamp if isinstance(timestamp, int) else _utils.datetime_to_ms(timestamp)
        self.value = value


class TimeseriesWithDatapoints(object):
    "Data transfer object for a timeseries with datapoints.\n\n    Attributes:\n        tag_id (str):       Unique ID of time series.\n        datapoints (List[v05.dto.Datapoint]): List of datapoints in the timeseries.\n    "

    def __init__(self, name, datapoints):
        self.name = name
        self.datapoints = datapoints


class LatestDatapointResponse(CogniteDataObject):
    "Latest Datapoint Response Object."

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"][0]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        return pd.DataFrame([self.internal_representation["data"]["items"][0]])

    def to_ndarray(self):
        "Returns data as a numpy array"
        return self.to_pandas().values[0]


class TimeSeriesResponse(CogniteDataObject):
    "Time series Response Object"

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        items = deepcopy(self.internal_representation["data"]["items"])
        if items and (items[0].get("metadata") is None):
            return pd.DataFrame(items)
        for d in items:
            if d.get("metadata"):
                d.update(d.pop("metadata"))
        return pd.DataFrame(items)


class TimeSeries(object):
    "Data Transfer Object for a time series.\n\n    Attributes:\n        name (str):       Unique name of time series.\n        isString (bool):    Whether the time series is string valued or not.\n        metadata (dict):    Metadata.\n        unit (str):         Physical unit of the time series.\n        assetId (str):     Asset that this time series belongs to.\n        description (str):  Description of the time series.\n        securityCategories (list(int)): Security categories required in order to access this time series.\n        isStep (bool):        Whether or not the time series is a step series.\n\n    "

    def __init__(
        self,
        name,
        is_string=False,
        metadata=None,
        unit=None,
        asset_id=None,
        description=None,
        security_categories=None,
        is_step=None,
    ):
        self.name = name
        self.isString = is_string
        self.metadata = metadata
        self.unit = unit
        self.assetId = asset_id
        self.description = description
        self.securityCategories = security_categories
        self.isStep = is_step


class AssetListResponse(CogniteDataObject):
    "Assets Response Object"

    def __init__(self, internal_representation):
        super().__init__(internal_representation)
        self.counter = 0

    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        if len(self.to_json()) > 0:
            return pd.DataFrame(self.internal_representation["data"]["items"])
        return pd.DataFrame()

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter > (len(self.to_json()) - 1):
            raise StopIteration
        else:
            self.counter += 1
            return AssetResponse({"data": {"items": [self.to_json()[(self.counter - 1)]]}})


class AssetResponse(CogniteDataObject):
    def to_json(self):
        "Returns data as a json object"
        return self.internal_representation["data"]["items"][0]

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        if len(self.to_json()) > 0:
            return pd.DataFrame.from_dict(self.to_json(), orient="index")
        return pd.DataFrame()


class Asset(object):
    "Data transfer object for assets.\n\n    Attributes:\n        name (str):                 Name of asset. Often referred to as tag.\n        parent_id (int):            ID of parent asset, if any.\n        description (str):          Description of asset.\n        metadata (dict):            Custom , application specific metadata. String key -> String Value.\n        ref_id (str):               Reference ID used only in post request to disambiguate references to duplicate\n                                    names.\n        parent_name (str):          Name of parent, this parent must exist in the same POST request.\n        parent_ref_id (list(int)):  Reference ID of parent, to disambiguate if multiple nodes have the same name.\n    "

    def __init__(
        self, name, parent_id=None, description=None, metadata=None, ref_id=None, parent_name=None, parent_ref_id=None
    ):
        self.name = name
        self.parentId = parent_id
        self.description = description
        self.metadata = metadata
        self.refId = ref_id
        self.parentName = parent_name
        self.parentRefId = parent_ref_id


class FileInfoResponse(CogniteDataObject):
    "File Info Response Object.\n\n    Attributes:\n        id (int):               ID given by the API to the file.\n        file_name (str):        File name. Max length is 256.\n        directory (str):        Directory containing the file. Max length is 512.\n        source (dict):          Source that this file comes from. Max length is 256.\n        file_type (str):        File type. E.g. pdf, css, spreadsheet, .. Max length is 64.\n        metadata (dict):        Customized data about the file.\n        asset_ids (list[str]):  Names of assets related to this file.\n        uploaded (bool):        Whether or not the file is uploaded.\n        uploaded_at (int):      Epoc thime (ms) when the file was uploaded succesfully.\n    "

    def __init__(self, internal_representation):
        super().__init__(internal_representation)
        item = self.internal_representation["data"]["items"][0]
        self.id = item.get("id")
        self.file_name = item.get("fileName")
        self.directory = item.get("directory")
        self.source = item.get("source")
        self.file_type = item.get("fileType")
        self.metadata = item.get("metadata")
        self.asset_ids = item.get("assetIds")
        self.uploaded = item.get("uploaded")
        self.uploaded_at = item.get("uploadedAt")

    def to_json(self):
        return self.internal_representation["data"]["items"][0]

    def to_pandas(self):
        file_info = deepcopy(self.to_json())
        if file_info.get("metadata"):
            file_info.update(file_info.pop("metadata"))
        return pd.DataFrame.from_dict(file_info, orient="index")


class FileListResponse(CogniteDataObject):
    "File List Response Object"

    def to_json(self):
        return self.internal_representation["data"]["items"]

    def to_pandas(self):
        return pd.DataFrame(self.internal_representation["data"]["items"])


class EventResponse(CogniteDataObject):
    "Event Response Object."

    def __init__(self, internal_representation):
        super().__init__(internal_representation)
        item = self.internal_representation["data"]["items"][0]
        self.id = item.get("id")
        self.asset_ids = item.get("assetIds")

    def to_json(self):
        return self.internal_representation["data"]["items"][0]

    def to_pandas(self):
        event = deepcopy(self.to_json())
        if event.get("metadata"):
            event.update(event.pop("metadata"))
        return pd.DataFrame.from_dict(event, orient="index")


class EventListResponse(CogniteDataObject):
    "Event List Response Object."

    def __init__(self, internal_representation):
        super().__init__(internal_representation)
        self.counter = 0

    def to_json(self):
        return self.internal_representation["data"]["items"]

    def to_pandas(self):
        items = deepcopy(self.to_json())
        for d in items:
            if d.get("metadata"):
                d.update(d.pop("metadata"))
        return pd.DataFrame(items)

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter > (len(self.to_json()) - 1):
            raise StopIteration
        else:
            self.counter += 1
            return EventResponse({"data": {"items": [self.to_json()[(self.counter - 1)]]}})


class Event(object):
    "Data transfer object for events.\n    Attributes:\n        start_time (int):       Start time of the event in ms since epoch.\n        end_time (int):         End time of the event in ms since epoch.\n        description (str):      Textual description of the event.\n        type (str):             Type of the event, e.g. 'failure'.\n        sub_type (str):          Subtype of the event, e.g. 'electrical'.\n        metadata (dict):        Customizable extra data about the event.\n        asset_ids (list[int]):  List of Asset IDs of related equipments that this event relates to.\n    "

    def __init__(
        self, start_time=None, end_time=None, description=None, type=None, sub_type=None, metadata=None, asset_ids=None
    ):
        self.startTime = start_time
        self.endTime = end_time
        self.description = description
        self.type = type
        self.subtype = sub_type
        self.metadata = metadata
        self.assetIds = asset_ids
