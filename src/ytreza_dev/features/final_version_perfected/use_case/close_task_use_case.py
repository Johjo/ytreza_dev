from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskNever, TaskNew, TaskNext, TaskBase


class CloseTaskUseCase:
    def __init__(self, task_repository: TaskRepositoryPort) -> None:
        self._task_repository = task_repository

    def execute(self, url: str) -> None:
        after, before = self._extract_task_before_closed_task(self._task_repository.all_tasks(), url)
        after += self._update_task_following_closed_task(before)
        if all(isinstance(task, TaskNever) for task in after):
            after = [task.to_new() for task in after]
        self._task_repository.save(after)

    @staticmethod
    def _update_task_following_closed_task(before: list[TaskBase]) -> list[TaskBase]:
        after_bis = []
        for task in before:
            if isinstance(task, TaskNever):
                after_bis.append(task)
            else:
                after_bis.append(task.to_new())
        return after_bis

    @staticmethod
    def _extract_task_before_closed_task(before: list[TaskBase], url: str) -> tuple[list[TaskBase], list[TaskBase]]:
        after = []
        # on garde toutes les tâches avant la tâche à fermer
        i = 0
        while before[i].url != url:
            after.append(before[i])
            i += 1
        # on ignore la tâche fermée
        before = before[i + 1:]
        return after, before
