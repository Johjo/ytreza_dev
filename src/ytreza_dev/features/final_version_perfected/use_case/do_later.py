from ytreza_dev.features.final_version_perfected.port.task_repository import TaskFvpRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase


class DoLater:
    def __init__(self, task_repository: TaskFvpRepositoryPort) -> None:
        self._task_repository = task_repository

    def execute(self, updated_key: str) -> None:
        before : list[TaskBase] = self._task_repository.all_tasks()

        self._task_repository.save([before[0].to_next()] + [self._update_task(task, updated_key) for task in before[1:]])

    @staticmethod
    def _update_task(task: TaskBase, updated_key: str) -> TaskBase:
        if task.id != updated_key:
            return task

        return task.to_later()
