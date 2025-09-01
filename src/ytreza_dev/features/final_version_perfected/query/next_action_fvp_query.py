from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformationReaderPort
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.types import TaskDetail, NothingToDo, DoTheTask, ChooseTaskBetween, \
    NextAction, \
    TaskNew, TaskNext, TaskBase


class NextActionFvpQuery:
    def __init__(self, task_fvp_reader: TaskFvpReaderPort, task_information_reader: TaskInformationReaderPort):
        self._task_fvp_reader = task_fvp_reader
        self._task_information_reader = task_information_reader

    def next_action(self) -> NextAction:
        tasks = self._task_fvp_reader.all_active_tasks()

        if not tasks:
            return NothingToDo()

        next_task_index = self._next_task_index(tasks)
        new_task_index = self._new_task_index(next_task_index, tasks)

        next_task = tasks[next_task_index]
        if new_task_index > next_task_index:
            new_task = tasks[new_task_index]
            return self._choose_action(new_task, next_task)

        return self._do_action(next_task)

    def _do_action(self, next_task):
        return DoTheTask(task=self._to_task_detail(next_task))

    def _choose_action(self, new_task, next_task):
        return ChooseTaskBetween(tasks=(
            self._to_task_detail(next_task),
            self._to_task_detail(new_task)
        ))

    def _to_task_detail(self, task):
        task_information = self._task_information_reader.by_key(task.id)
        return TaskDetail(
            key=task.id,
            title=task_information.title,
            url=task_information.url,
            project_name=task_information.project.name,
            due_date=task_information.due_date
        )

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
                next((index for index, task in list(enumerate(tasks)) if isinstance(task, TaskNew)),
                0)
        )
