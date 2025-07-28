from abc import ABCMeta, abstractmethod

from ytreza_dev.features.todolist_query_fvp.types import Task, NothingToDo, DoTheTask, ChooseTaskBetween, NextAction, \
    TaskNew, TaskNext, TaskBase


class TaskReader(metaclass=ABCMeta):
    @abstractmethod
    def all_active_tasks(self) -> list[TaskBase]:
        pass


class NextActionFvpQuery:
    def __init__(self, task_reader: TaskReader):
        self._task_reader = task_reader

    def next_action(self) -> NextAction:
        tasks = self._task_reader.all_active_tasks()

        if not tasks:
            return NothingToDo()

        next_task_index = self._next_task_index(tasks)
        new_task_index = self._new_task_index(next_task_index, tasks)

        if new_task_index > next_task_index:
            return ChooseTaskBetween(tasks=(
                Task(title=tasks[next_task_index].title, url=tasks[next_task_index].url),
                Task(title=tasks[new_task_index].title, url=tasks[new_task_index].url)
            ))

        return DoTheTask(task=Task(title=tasks[next_task_index].title, url=tasks[next_task_index].url))

    @staticmethod
    def _new_task_index(next_task_index: int, tasks: list[TaskBase]) -> int:
        return next(
            (index for index in range(next_task_index + 1, len(tasks)) if isinstance(tasks[index], TaskNew)),
            next_task_index
        )

    @staticmethod
    def _next_task_index(tasks: list[TaskBase]) -> int:
        return next(
                (index for index, task in reversed(list(enumerate(tasks))) if isinstance(task, TaskNext)),
                0
        )
