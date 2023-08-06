
"Models Module.\n\nThis module mirrors the Models API.\n\nhttps://doc.cognitedata.com/0.6/models\n"
import requests
from cognite import _utils as utils
from cognite import config


def create_model(name, description="", metadata=None, input_fields=None, output_fields=None, **kwargs):
    "Creates a new hosted model\n\n    Args:\n        name (str):             Name of model\n        description (str):      Description\n        metadata (Dict[str, Any]):          Metadata about model\n        input_fields (List[str]):   List of input fields the model accepts\n        output_fields (List[str]:   List of output fields the model produces\n\n    Returns:\n        The created model.\n    "
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models".format(project)
    headers = {"api-key": api_key, "accept": "application/json"}
    model_body = {
        "name": name,
        "description": description,
        "metadata": (metadata or {}),
        "inputFields": (input_fields or []),
        "outputFields": (output_fields or []),
    }
    res = utils.post_request(url, body=model_body, headers=headers, cookies=config.get_cookies())
    return res.json()


def get_models(**kwargs):
    "Get all models."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models".format(project)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.get_request(url, headers=headers, cookies=config.get_cookies())
    return res.json()


def get_model_versions(model_id, **kwargs):
    "Get all versions of a specific model."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models/{}/versions".format(project, model_id)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.get_request(url, headers=headers, cookies=config.get_cookies())
    return res.json()


def delete_model(model_id, **kwargs):
    "Delete a model."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models/{}".format(project, model_id)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.delete_request(url, headers=headers, cookies=config.get_cookies())
    return res.json()


def train_model_version(
    model_id,
    name,
    description=None,
    predict_source_package_id=None,
    train_source_package_id=None,
    args=None,
    scale_tier=None,
    machine_type=None,
    **kwargs
):
    "Train a new version of a model."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models/{}/versions/train".format(project, model_id)
    body = {
        "name": name,
        "description": (description or ""),
        "sourcePackageID": predict_source_package_id,
        "trainingDetails": {
            "sourcePackageID": (train_source_package_id or predict_source_package_id),
            "args": (args or {}),
            "scaleTier": (scale_tier or "BASIC"),
            "machineType": machine_type,
        },
    }
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.post_request(url, body=body, headers=headers, cookies=config.get_cookies())
    return res.json()


def online_predict(model_id, version_id=None, instances=None, arguments=None, **kwargs):
    "Perform online prediction on a models active version or a specified version."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    if version_id:
        url = config.get_base_url() + "/api/0.6/projects/{}/models/{}/versions/{}/predict".format(
            project, model_id, version_id
        )
    else:
        url = config.get_base_url() + "/api/0.6/projects/{}/models/{}/predict".format(project, model_id)
    body = {"instances": instances, "arguments": (arguments or {})}
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.put_request(url, body=body, headers=headers, cookies=config.get_cookies())
    return res.json()


def get_model_source_packages(**kwargs):
    "Get all model source packages."
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models/sourcepackages".format(project)
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.get_request(url, headers=headers, cookies=config.get_cookies())
    return res.json()


def upload_source_package(
    name, description, package_name, available_operations, meta_data=None, file_path=None, **kwargs
):
    'Upload a source package to the model hosting environment.\n\n    Args:\n        name: Name of source package\n        description: Description for source package\n        package_name: name of root package for model\n        available_operations: List of routines which this source package supports ["predict", "train"]\n        meta_data: User defined key value pair of additional information.\n        file_path (str): File path of source package distribution. If not sepcified, a download url will be returned.\n        **kwargs:\n\n    Returns:\n        Source package ID if file path was specified. Else, source package id and upload url.\n\n    '
    (api_key, project) = config.get_config_variables(kwargs.get("api_key"), kwargs.get("project"))
    url = config.get_base_url() + "/api/0.6/projects/{}/models/sourcepackages".format(project)
    body = {
        "name": name,
        "description": (description or ""),
        "packageName": package_name,
        "availableOperations": available_operations,
        "metadata": (meta_data or {}),
    }
    headers = {"api-key": api_key, "accept": "application/json"}
    res = utils.post_request(url, body=body, headers=headers, cookies=config.get_cookies())
    if file_path:
        _upload_file(res.json().get("uploadURL"), file_path)
        del res.json()["uploadURL"]
        return res.json()
    return res.json()


def _upload_file(upload_url, file_path):
    with open(file_path, "rb") as fh:
        mydata = fh.read()
        response = requests.put(upload_url, data=mydata)
    return response
