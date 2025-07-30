import os

from dotenv import load_dotenv
from approvaltests import verify

from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


def test_all_tasks() -> None:
    load_dotenv(dotenv_path=".env.test")
    api_token = os.getenv("TODOIST_API_TOKEN")
    assert api_token, "TODOIST_API_TOKEN not found in .env.test"

    todoist_api = TodoistAPI(api_token)
    tasks = todoist_api.get_all_tasks()
    verify("\n".join([str(task) for task in tasks]), encoding="utf-8")
