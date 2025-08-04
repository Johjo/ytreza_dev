from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew


class ChooseTaskUseCase:
    def __init__(self, task_repository: TaskRepositoryPort):
        self._task_repository = task_repository

    def execute(self, url: str) -> None:
        all_tasks_before = self._task_repository.all_tasks()
        all_tasks_after : list[TaskBase] = []

        all_tasks_after.append(all_tasks_before[0].to_next())

        first_new_index = self._first_new_index(all_tasks_before[1:]) + 1
        i = 1

        while len(all_tasks_before) > i:
            if url == all_tasks_before[i].url:
                all_tasks_after.append(all_tasks_before[i].to_next())
            else:
                if i != first_new_index:
                    all_tasks_after.append(all_tasks_before[i])
                else:
                    all_tasks_after.append(all_tasks_before[i].to_later())
            i += 1

        self._task_repository.save(all_tasks_after)

    @staticmethod
    def _first_new_index(all_tasks_before: list[TaskBase]) -> int:
        for index, task in enumerate(all_tasks_before):
            if isinstance(task, TaskNew):
                return index

        raise NotImplementedError()
