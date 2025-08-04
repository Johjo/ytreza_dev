from pathlib import Path

from dotenv import load_dotenv

from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.start_fvp_use_case.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase
from ytreza_dev.shared.env_reader import EnvReaderFromEnv


def test_full_synchronisation_from_todoist_to_json() -> None:
    load_dotenv(dotenv_path=".env")
    StartFvpUseCase(todolist_reader=TodolistReaderFromTodoist(EnvReaderFromEnv()), task_repository=TaskRepositoryFromJson(file_path=Path("data_test/tasks.json"))).execute()
