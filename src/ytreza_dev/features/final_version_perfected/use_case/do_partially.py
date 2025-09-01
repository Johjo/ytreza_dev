from ytreza_dev.features.final_version_perfected.port.task_repository import TaskFvpRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskLater, TaskNew


class DoPartially:
    def __init__(self, task_repository: TaskFvpRepositoryPort) -> None:
        self._task_repository = task_repository

    def execute(self, updated_key: str) -> None:
        before = self._task_repository.all_tasks()
        if before[0].id == updated_key:
            after = self._first_task_done_partially(before)
        else:
            after = self._another_task_done_partially(before, updated_key)

        self._task_repository.save(after)

    def _another_task_done_partially(self, before: list[TaskBase], updated_key: str):
        after = []
        index = 0
        after.append(before[index].to_next())
        index += 1
        while len(before) > index and before[index].id != updated_key:
            after.append(before[index])
            index += 1
        after.append(before[index].to_later())
        index += 1

        while len(before) > index:
            if isinstance(before[index], TaskLater):
                after.append(before[index].to_new())
            else:
                after.append(before[index])
            index += 1
        return after


    def _first_task_done_partially(self, before: list[TaskBase]) -> list[TaskBase]:
        after = []
        index = 0
        after.append(before[index].to_next())
        index += 1
        while len(before) > index and not isinstance(before[index], TaskNew):
            after.append(before[index])
            index += 1
        if len(before) > index:
            after.append(before[index].to_next())
            index += 1

        after.extend(before[index:])

        return after
