from pyqure import Key # type: ignore

from ytreza_dev.features.start_fvp_use_case.use_case import TaskRepository
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import TaskReader
from ytreza_dev.shared.final_version_perfected.types import TaskBase


class TaskInMemory:
    def __init__(self) -> None:
        self._tasks: list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks


TASK_IN_MEMORY_KEY = Key("task_in_memory", TaskInMemory)


class TaskRepositoryForDemo(TaskRepository):
    def all_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()

    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def save(self, tasks: list[TaskBase]) -> None:
        self._memory.save(tasks)


class TaskReaderForDemo(TaskReader):
    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def all_active_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()
