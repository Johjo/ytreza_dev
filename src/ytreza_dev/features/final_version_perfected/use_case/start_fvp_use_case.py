from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import TaskNew


class StartFvpUseCase:
    def __init__(self, todolist_reader: TodolistReaderPort, task_repository: TaskRepositoryPort) -> None:
        self._todolist_reader = todolist_reader
        self._task_repository = task_repository

    def execute(self) -> None:
        self._task_repository.save([TaskNew(title=task.name, url=task.url) for task in self._todolist_reader.all_tasks()])
