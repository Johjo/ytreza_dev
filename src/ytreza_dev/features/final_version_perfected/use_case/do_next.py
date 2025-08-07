from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNever


class DoNext:
    def __init__(self, task_repository: TaskRepositoryPort):
        self._task_repository = task_repository

    def execute(self, url: str) -> None:
        before: list[TaskBase] = self._task_repository.all_tasks()

        self._task_repository.save([self._update_first_task(before)] + [self.update_task(task, url) for task in before[1:]])

    @staticmethod
    def _update_first_task(before: list[TaskBase]) -> TaskBase:
        if isinstance(before[0], TaskNever):
            return before[0]
        return before[0].to_next()

    @staticmethod
    def update_task(task: TaskBase, url: str) -> TaskBase:
        if task.url != url:
            return task
        return task.to_next()
