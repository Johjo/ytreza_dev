from abc import ABC, abstractmethod

from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformation


class TaskInformationRepositoryPort(ABC):
    @abstractmethod
    def save(self, task: TaskInformation) -> None: ...
