from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass
class Task:
    name: str
    url: str


class TaskRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, tasks: list[Task]) -> None:
        pass


class TodolistReader(metaclass=ABCMeta):
    @abstractmethod
    def all_tasks(self) -> list[Task]:
        pass


class StartFvpUseCase:
    def __init__(self, todolist_reader: TodolistReader, task_repository: TaskRepository) -> None:
        self._todolist_reader = todolist_reader
        self._task_repository = task_repository

    def execute(self) -> None:
        self._task_repository.save(self._todolist_reader.all_tasks())
