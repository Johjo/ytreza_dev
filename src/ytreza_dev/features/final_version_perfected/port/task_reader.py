from abc import ABCMeta, abstractmethod

from ytreza_dev.features.final_version_perfected.types import TaskBase


class TaskFvpReaderPort(metaclass=ABCMeta):
    @abstractmethod
    def all_active_tasks(self) -> list[TaskBase]:
        pass
