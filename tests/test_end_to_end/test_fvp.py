from pathlib import Path

from ytreza_dev.shared.env_reader import EnvReaderFromEnv, EnvReaderPort
from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.start_fvp_use_case.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase
from dotenv import load_dotenv

def test_xxx():
    load_dotenv(dotenv_path=".env")
    StartFvpUseCase(todolist_reader=TodolistReaderFromTodoist(EnvReaderFromEnv()), task_repository=TaskRepositoryFromJson(file_path=Path("data_test/tasks.json"))).execute()
