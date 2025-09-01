from abc import ABCMeta, abstractmethod

from ytreza_dev.features.final_version_perfected.types import TaskBase


class TaskFvpRepositoryPort(metaclass=ABCMeta):
    @abstractmethod
    def save(self, tasks: list[TaskBase]) -> None:
        pass

    @abstractmethod
    def all_tasks(self) -> list[TaskBase]:
        pass
