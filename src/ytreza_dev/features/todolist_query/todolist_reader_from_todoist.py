import os
import requests
from dotenv import load_dotenv

from ytreza_dev.features.todolist_query.todolist_query import TodolistReaderPort, Task

load_dotenv()


class TodolistReaderFromTodoist(TodolistReaderPort):
    def __init__(self):
        self.api_token = os.getenv("TODOIST_API_TOKEN")
        if not self.api_token:
            raise ValueError("TODOIST_API_TOKEN environment variable not set.")
        self.api_url = "https://api.todoist.com/rest/v2"

    def all_tasks(self) -> list[Task]:
        headers = {
            "Authorization": f"Bearer {self.api_token}",
        }
        response = requests.get(f"{self.api_url}/tasks", headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        tasks_data = response.json()
        return [Task(name=task_data["content"], url=task_data["url"]) for task_data in tasks_data]

