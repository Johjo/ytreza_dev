from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from ytreza_dev.shared.final_version_perfected.types import TaskBase, TaskNew


@dataclass
class OldTask:
    name: str
    url: str


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, tasks: list[TaskBase]) -> None:
        pass

@dataclass
class ExternalTask:
    name: str
    url: str


class TodolistReader(metaclass=ABCMeta):
    @abstractmethod
    def all_tasks(self) -> list[ExternalTask]:
        pass


class StartFvpUseCase:
    def __init__(self, todolist_reader: TodolistReader, task_repository: TaskRepository) -> None:
        self._todolist_reader = todolist_reader
        self._task_repository = task_repository

    def execute(self) -> None:
        self._task_repository.save([TaskNew(title=task.name, url=task.url) for task in self._todolist_reader.all_tasks()])
