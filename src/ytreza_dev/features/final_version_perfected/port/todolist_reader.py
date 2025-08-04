from abc import ABCMeta, abstractmethod

from ytreza_dev.features.final_version_perfected.types import ExternalTask


class TodolistReaderPort(metaclass=ABCMeta):
    @abstractmethod
    def all_tasks(self) -> list[ExternalTask]:
        pass
