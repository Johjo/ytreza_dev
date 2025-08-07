from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskNever, TaskBase


class CloseTaskUseCase:
    def __init__(self, task_repository: TaskRepositoryPort, external_todolist: ExternalTodolistPort) -> None:
        self._external_todolist = external_todolist
        self._task_repository = task_repository

    def execute(self, url: str) -> None:
        after, before = self._extract_task_before_closed_task(self._task_repository.all_tasks(), url)
        after += self._update_task_following_closed_task(before)
        if all(isinstance(task, TaskNever) for task in after):
            after = [task.to_new() for task in after]
        self._task_repository.save(after)
        self._external_todolist.close_task(url=url)

    @staticmethod
    def _update_task_following_closed_task(before: list[TaskBase]) -> list[TaskBase]:
        after : list[TaskBase] = []
        for task in before:
            if isinstance(task, TaskNever):
                after.append(task)
            else:
                after.append(task.to_new())
        return after

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
