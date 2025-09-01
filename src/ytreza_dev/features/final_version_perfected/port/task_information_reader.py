import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass

from expression import Option

from ytreza_dev.features.final_version_perfected.types import Project


@dataclass
class TaskInformation:
    key: str
    url: str
    title: str
    project: Project
    due_date: Option[datetime.date]



class TaskInformationReaderPort(ABC):
    @abstractmethod
    def by_key(self, key: str) -> TaskInformation:
        ...