import os

from approvaltests import verify # type: ignore
from dotenv import load_dotenv

from ytreza_dev.features.final_version_perfected.adapter.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.shared.env_reader import EnvReaderFromEnv


def test_all_tasks() -> None:
    todoist_api = TodolistReaderFromTodoist(EnvReaderFromEnv(env_path=".env.test"))
    tasks = todoist_api.all_tasks()

    verify("\n".join([str(task) for task in tasks]), encoding="utf-8")
