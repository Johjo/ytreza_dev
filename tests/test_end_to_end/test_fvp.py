from pathlib import Path

from dotenv import load_dotenv

from ytreza_dev.features.final_version_perfected.use_case.start_fvp_use_case import StartFvpUseCase
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.final_version_perfected.adapter.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.shared.env_reader import EnvReaderFromEnv


def test_full_synchronisation_from_todoist_to_json() -> None:
    StartFvpUseCase(todolist_reader=TodolistReaderFromTodoist(EnvReaderFromEnv(".env")), task_repository=TaskRepositoryFromJson(file_path=Path("data_test/tasks.json"))).execute()
