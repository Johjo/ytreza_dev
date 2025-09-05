from expression import Nothing
from pyqure import Key

from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformationRepositoryPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.port.task_repository import FvpRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, ExternalTask


class TaskInMemory:
    def __init__(self) -> None:
        self._tasks: list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks


class TaskFvpReaderForDemo(TaskFvpReaderPort):
    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def all_active_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()


class FvpRepositoryForDemo(FvpRepositoryPort):
    def all_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()

    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def save(self, tasks: list[TaskBase]) -> None:
        self._memory.save(tasks)


TASK_IN_MEMORY_KEY = Key("task_in_memory", TaskInMemory)


class ExternalTodolistForDemo(ExternalTodolistPort):
    def close_task(self, url: str, task_id: str) -> None:
        pass


class TaskInformationRepositoryForDemo(TaskInformationRepositoryPort):
    def __init__(self):
        self._tasks: dict[str, TaskInformation] = {}

    def by_key(self, key: str) -> TaskInformation:
        return self._tasks[key]

    def save(self, task: list[TaskInformation]) -> None:
        for task in task:
            self._tasks[task.key] = task
