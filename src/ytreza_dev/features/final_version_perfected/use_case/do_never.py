from ytreza_dev.features.final_version_perfected.types import TaskBase


class DoNever:
    def __init__(self, task_repository):
        self._task_repository = task_repository

    def execute(self, url: str):
        before : list[TaskBase] = self._task_repository.all_tasks()

        self._task_repository.save([before[0].to_next()] + [self._update_task(task, url) for task in before[1:]])

    @staticmethod
    def _update_task(task: TaskBase, url):
        if task.url != url:
            return task

        return task.to_never()
