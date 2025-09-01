from abc import ABC, abstractmethod
from dataclasses import dataclass

from ytreza_dev.features.final_version_perfected.types import Project


@dataclass
class TaskInformation:
    key: str
    title: str
    project: Project



class TaskInformationReaderPort(ABC):
    @abstractmethod
    def by_key(self, key: str) -> TaskInformation:
        ...