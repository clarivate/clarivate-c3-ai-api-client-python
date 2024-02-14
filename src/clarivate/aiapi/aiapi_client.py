#-- Version: 0.0.1
#-- Script which helps create ai api client and use ai api endpoint easily

import os
import sys
from pathlib import Path
import shutil
from typing import Any, Optional

import httpx
from platformdirs import user_config_dir, user_data_dir


# Autovivify our application's private directory
MODULE_DIR = Path(__file__).parent
PRIVATE_DIR = Path(user_config_dir("aiapi", "clarivate"))
if not PRIVATE_DIR.exists():
    os.makedirs(PRIVATE_DIR)
else:
    if not PRIVATE_DIR.is_dir():
        sys.stderr.write(f"Error: {PRIVATE_DIR} is a file, but should be a directory!\n")
        sys.exit(1)
if not (PRIVATE_DIR / "config.py").exists():
    shutil.copy(MODULE_DIR / "config.py", PRIVATE_DIR)

# Import our config
sys.path.insert(0, str(PRIVATE_DIR.absolute()))
import config
sys.path=sys.path[1:]

Logs = list[tuple[str, str]]
Response = Any

class MissingAuth(Exception):
    def __str__(self):
        return "No API key found! Please specify as the environment variable AI_API_KEY or pass to Client initializer."

class Client():
    def __init__(self, api_key: str, server_url: str = 'https://api.clarivate.com/') -> None:
        if not api_key:
            raise ValueError("api_key has to be defined instead of None!")

        self.api_key = api_key or config.API_KEY
        self.server_url = server_url or config.SERVER_URL
        if not self.api_key:
            raise MissingAuth

        self.endpoint_name_info = "c3/ai/info/"
        self.endpoint_name_ontology = "c3/ai/ontology/" 
        self.endpoint_name_prediction = "c3/ai/prediction"
        self.logs: Logs = []


    def __add_to_log(self, logmsg: tuple[str, str]):
        self.logs.append(logmsg)


    def __make_request(self, endpoint: str, payload: Optional[dict[str, Any]] = None) -> httpx.Response:
        auth_headers = {
            "X-ApiKey": self.api_key
        }

        base_url = endpoint
        data = payload if payload else None

        try:
            if data:
                response = httpx.post(base_url, json=data, headers=auth_headers, follow_redirects=True)
            else:
                response = httpx.get(base_url, headers=auth_headers, follow_redirects=True)
        except httpx.RequestError as e:
            self.__add_to_log(('FAILURE',f'Issue with request to endpoint {base_url} due to {e}'))
            return None

        return response

    def __contentset_checker(self, content_set_name: Optional[str]) -> bool:
        if content_set_name and content_set_name not in config.CONTENT_SET_NAMES:
            self.__add_to_log(('FAILURE','Issue with content_set_name'))
            return False
        return True

    def __process_response(self, url: str, inputs: Optional[dict[str, Any]] = None) -> tuple[Response, Logs]:
        response = self.__make_request(url, inputs) if inputs else self.__make_request(url)
        if response:
            if response.status_code != httpx.codes.OK:
                self.__add_to_log(('FAILURE',f'Issue with request to endpoint {url} due to {response.text}'))
                return None, self.logs
            else:
                try:
                    response_data = response.json()
                    self.__add_to_log(('SUCCESS',f'Successfully receive response from endpoint {url}'))
                    return response_data, self.logs
                except Exception as e:
                    self.__add_to_log(('FAILURE',f'Unexpected error when reading response from endpoint {url} due to {e}, raw response: {response.text}'))
                    return None, self.logs

        return None, self.logs

 
    def info(self, content_set_name: str) -> tuple[Response, Logs]:
        if not self.__contentset_checker(content_set_name):
            return None, self.logs
        url = f"{self.server_url}{self.endpoint_name_info}{content_set_name}"
        return self.__process_response(url)


    def ontologies(self, content_set_name: str) -> tuple[Response, Logs]:
        if not self.__contentset_checker(content_set_name):
            return None, self.logs
        url = f"{self.server_url}{self.endpoint_name_ontology}{content_set_name}"
        return self.__process_response(url)


    def ontology(self, content_set_name: str, ontology: str, search: Optional[str] = None) -> tuple[Response, Logs]:
        if not self.__contentset_checker(content_set_name):
            return None, self.logs
        base_url = f"{self.server_url}{self.endpoint_name_ontology}{content_set_name}/{ontology}"
        url = base_url + f"?search={search}" if search else base_url
        return self.__process_response(url)


    def predictions(self, content_set_name: Optional[str] = None) -> tuple[Response, Logs]:
        if not self.__contentset_checker(content_set_name):
            return None, self.logs
        base_url = f"{self.server_url}{self.endpoint_name_prediction}"
        url = base_url + f"?contentset={content_set_name}" if content_set_name else base_url
        return self.__process_response(url)


    def predict(self, prediction_name: str, inputs: dict[str, Any]) -> tuple[Response, Logs]:
        url = f"{self.server_url}{self.endpoint_name_prediction}/{prediction_name}"
        return self.__process_response(url, inputs)
