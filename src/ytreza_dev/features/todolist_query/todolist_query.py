from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

@dataclass
class Task:
    name: str
    url: str


class TodolistReaderPort(metaclass=ABCMeta):
    @abstractmethod
    def all_tasks(self) -> list[Task]:
        pass


class TodolistQuery:
    def __init__(self, todolist_reader: TodolistReaderPort):
        self._todolist_reader = todolist_reader

    def all_tasks(self) -> list[Task]:
        return self._todolist_reader.all_tasks()
