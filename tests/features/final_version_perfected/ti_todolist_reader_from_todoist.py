import os

from approvaltests import verify # type: ignore
from dotenv import load_dotenv

from ytreza_dev.features.start_fvp_use_case.todolist_reader_from_todoist import TodolistReaderFromTodoist


def test_all_tasks() -> None:
    load_dotenv(dotenv_path=".env.test")
    api_token = os.getenv("TODOIST_API_TOKEN")
    assert api_token, "TODOIST_API_TOKEN not found in .env.test"

    todoist_api = TodolistReaderFromTodoist()
    tasks = todoist_api.all_tasks()

    verify("\n".join([str(task) for task in tasks]), encoding="utf-8")
