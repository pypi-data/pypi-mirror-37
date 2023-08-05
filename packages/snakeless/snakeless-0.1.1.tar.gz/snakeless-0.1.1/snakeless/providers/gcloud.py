import json
import logging
import requests
from functools import partial

import fs
from fs.copy import copy_fs
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

from .base import BaseProvider
from ..exceptions import CommandFailure

logger = logging.getLogger(__name__)

logging.getLogger("google").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class GCloudApi(object):
    domain = "https://cloudfunctions.googleapis.com"
    create_function = {
        "path": "/v1/projects/{project_id}/locations/{location_id}/functions",
        "default_method": "POST",
    }
    update_function = {
        "path": "/v1/projects/{project_id}/locations/{location_id}/functions/{function_id}",  # noqa
        "default_method": "PATCH",
    }
    upload_code = {
        "path": (
            "/v1/projects/{project_id}/locations/{location_id}/functions:generateUploadUrl"  # noqa
        ),
        "default_method": "POST",
    }

    def call(
        self, endpoint, path_kwargs={}, session=requests.Session(), **kwargs
    ):
        method = kwargs.pop("method", endpoint.get("default_method", "GET"))
        endpoint_type = endpoint.get("response_type", "json")
        url = self.domain + endpoint["path"].format(**path_kwargs)
        r = session.request(method, url, **kwargs)
        if endpoint_type == "json":
            return r.json()
        return r.text


class GCloudProvider(BaseProvider):
    def __init__(self, config):
        self.config = config
        service_account_info = None
        with fs.open_fs(".") as root_fs:
            service_account_info = json.loads(
                root_fs.gettext(self.config["project"]["creds"])
            )
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        self.session = AuthorizedSession(credentials)
        self.api = GCloudApi()

    def generate_resource_function(self, func_name):
        get_data = partial(self.get_func_or_project_data, func_name)
        get_func_data = partial(self.get_func_data, func_name)
        project_id = self.get_project_data("name")
        location_id = get_data("region")
        deploy_func_name = get_func_data(
            "deploy_name", get_func_data("handler")
        )
        env_variables = self.get_env_variables(func_name)
        source_url = self.upload_func(func_name)
        resource_function = {
            "name": "projects/{0}/locations/{1}/functions/{2}".format(
                project_id, location_id, deploy_func_name
            ),
            "description": get_func_data("description", ""),
            "entryPoint": get_func_data("handler"),
            "runtime": get_data("runtime"),
            "timeout": str(get_data("timeout")) + "s",
            "availableMemoryMb": get_data("memory_size"),
            "labels": get_func_data("tags", {}),
            "environmentVariables": env_variables,
            "sourceUploadUrl": source_url,
            "httpsTrigger": {"url": get_func_data("path")},
        }
        return resource_function

    def package_code(self, config, func_name):
        handler_path = self.config["functions"][func_name]["handler_path"]
        with fs.open_fs(
            "./.snakeless/", create=True, writeable=True
        ) as root_fs:
            copy_fs(f"{handler_path}", f"zip://.snakeless/{func_name}.zip")
            return root_fs.getbytes(f"{func_name}.zip")

    def upload_func(self, func_name):
        packaged_code = self.package_code(self.config, func_name)

        response = self.api.call(
            self.api.upload_code,
            session=self.session,
            path_kwargs={
                "project_id": self.config["project"]["name"],
                "location_id": (
                    self.get_func_data(func_name, "region")
                    or self.config["project"]["region"]
                ),
            },
        )
        upload_url = response["uploadUrl"]
        r = requests.put(
            upload_url,
            headers={
                "content-type": "application/zip",
                "x-goog-content-length-range": "0,104857600",
            },
            data=packaged_code,
        )
        r.raise_for_status()
        return upload_url

    def deploy_function(
        self, func_name, resource_function=None, only_update=False
    ):
        resource_function = (
            resource_function
            if resource_function
            else self.generate_resource_function(func_name)
        )
        deploy_func_name = self.get_func_data(
            func_name, "deploy_name", self.get_func_data(func_name, "handler")
        )
        response = self.api.call(
            (
                self.api.update_function
                if only_update
                else self.api.create_function
            ),
            session=self.session,
            json=resource_function,
            path_kwargs={
                "project_id": self.config["project"]["name"],
                "location_id": (
                    self.get_func_data(func_name, "region")
                    or self.config["project"]["region"]
                ),
                "function_id": deploy_func_name
            },
        )
        if response.get("error"):
            if response["error"]["status"] == "ALREADY_EXISTS":
                return self.deploy_function(
                    func_name,
                    only_update=True,
                    resource_function=resource_function,
                )
            logger.error(response)
            raise CommandFailure("Function deployment has failed")
