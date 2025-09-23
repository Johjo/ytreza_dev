from toml.encoder import TomlPreserveInlineDictEncoder

from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ExternalTask, ExternalProject
from ytreza_dev.shared.env_reader import EnvReaderPort
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI, TodoistTask, TodoistProject


class TodolistReaderFromTodoist(TodolistReaderPort):
    def __init__(self, env_reader: EnvReaderPort):
        self._env_reader = env_reader

    def all_tasks(self) -> list[ExternalTask]:
        todoist = TodoistAPI(self._env_reader.read("TODOIST_API_TOKEN"))
        tasks = todoist.get_all_tasks()
        return [self._to_external_task(task) for task in tasks]

    def _to_external_task(self, task: TodoistTask):
        return ExternalTask(name=task.name, url=task.url, id=task.id, project=self._to_external_project(task.project), due_date=task.due_date)

    @staticmethod
    def _to_external_project(project: TodoistProject) -> ExternalProject:
        return ExternalProject(name=project.name, key=project.id)
