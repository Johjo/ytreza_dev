import json
from dataclasses import dataclass

import requests


@dataclass
class Task:
    name: str
    url: str


class TodoistAPI:
    def __init__(self, api_token: str):
        self._api_token = api_token
        self._base_url = "https://api.todoist.com/rest/v2"

    def get_all_tasks(self) -> list[Task]:
        headers = {
            "Authorization": f"Bearer {self._api_token}"
        }
        response = requests.get(f"{self._base_url}/tasks", headers=headers)
        response.raise_for_status()

        json_content = response.text
        tasks = json.loads(json_content)
        return [Task(name=task["content"], url=task["url"]) for task in tasks]
