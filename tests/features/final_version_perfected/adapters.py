from pyqure import Key # type: ignore

from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformationRepositoryPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.port.task_repository import FvpRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase


class FvpRepositoryForTest(FvpRepositoryPort):
    def __init__(self) -> None:
        self._tasks : list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks

    def feed(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks


class TaskInformationRepositoryForTest(TaskInformationRepositoryPort):
    def save(self, tasks: list[TaskInformation]) -> None:
        for task in tasks:
            self._tasks[task.key] = task

    def __init__(self):
        self._tasks: dict[str, TaskInformation] = {}

    def feed(self, tasks: list[TaskInformation]):
        for task in tasks:
            self._tasks[task.key] = task

    def by_key(self, key: str) -> TaskInformation:
        return self._tasks[key]

    def all_tasks(self) -> dict[str, TaskInformation]:
        return self._tasks
