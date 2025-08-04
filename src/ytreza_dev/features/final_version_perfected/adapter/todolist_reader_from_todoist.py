from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ExternalTask
from ytreza_dev.shared.env_reader import EnvReaderPort
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


class TodolistReaderFromTodoist(TodolistReaderPort):
    def __init__(self, env_reader: EnvReaderPort):
        self._env_reader = env_reader

    def all_tasks(self) -> list[ExternalTask]:
        todoist = TodoistAPI(self._env_reader.read("TODOIST_API_TOKEN"))
        tasks = todoist.get_all_tasks()
        return [ExternalTask(name=task.name, url=task.url) for task in tasks]
