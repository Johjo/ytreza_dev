import json
from dataclasses import dataclass
from typing import Any

import requests

@dataclass
class TodoistProject:
    id: str
    name: str


@dataclass
class TodoistTask:
    name: str
    url: str
    id: str
    project: TodoistProject


class TodoistAPI:
    def __init__(self, api_token: str):
        self._api_token = api_token
        self._base_url = "https://api.todoist.com/rest/v2"

    def get_all_tasks(self) -> list[TodoistTask]:
        tasks = json.loads(self._get_all_tasks_json())
        projects : dict[str, Any] = {p["id"]: p for p in json.loads(self._get_all_projects_json())}
        return [self._to_todoist_task(task, projects) for task in tasks]

    def _get_all_tasks_json(self):
        headers = {
            "Authorization": f"Bearer {self._api_token}"
        }
        response = requests.get(f"{self._base_url}/tasks", headers=headers)
        response.raise_for_status()
        json_content = response.text
        return json_content

    def _get_all_projects_json(self):
        headers = {
            "Authorization": f"Bearer {self._api_token}"
        }
        response = requests.get(f"{self._base_url}/projects", headers=headers)
        response.raise_for_status()
        json_content = response.text
        return json_content

    @staticmethod
    def _to_todoist_task(task, projects: [dict[str, Any]]):
        return TodoistTask(
            name=task["content"],
            url=task["url"],
            id=task["id"],
            project=TodoistProject(id=task["project_id"], name=projects[task["project_id"]]["name"])
        )

    def open_task(self, content: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self._base_url}/tasks", headers=headers, data=json.dumps({"content": content}))
        response.raise_for_status()

        json_content = response.text
        task = json.loads(json_content)
        return str(task["id"])

    def close_task(self, task_id: str) -> None:
        headers = {
            "Authorization": f"Bearer {self._api_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self._base_url}/tasks/{task_id}/close", headers=headers)
        response.raise_for_status()

    def task_by_id(self, task_id: str) -> TodoistTask:
        task = json.loads(self._json_task_by_id(task_id))
        projects: dict[str, Any] = {p["id"]: p for p in json.loads(self._get_all_projects_json())}
        return self._to_todoist_task(task, projects)

    def _json_task_by_id(self, task_id: str) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_token}"
        }
        response = requests.get(f"{self._base_url}/tasks/{task_id}", headers=headers)
        response.raise_for_status()
        json_content = response.text
        return json_content
