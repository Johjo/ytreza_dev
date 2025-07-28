import os

from approvaltests import verify
from dotenv import load_dotenv

from ytreza_dev.features.start_fvp_use_case.use_case import TodolistReader, Task
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


class TodolistReaderFromTodoist(TodolistReader):
    def all_tasks(self) -> list[Task]:
        todoist = TodoistAPI(os.getenv("TODOIST_API_TOKEN"))
        tasks = todoist.get_all_tasks()
        return [Task(name=task.name, url=task.url) for task in tasks]


def test_all_tasks() -> None:
    load_dotenv(dotenv_path=".env.test")
    api_token = os.getenv("TODOIST_API_TOKEN")
    assert api_token, "TODOIST_API_TOKEN not found in .env.test"

    todoist_api = TodolistReaderFromTodoist()
    tasks = todoist_api.all_tasks()

    verify("\n".join([str(task) for task in tasks]))
