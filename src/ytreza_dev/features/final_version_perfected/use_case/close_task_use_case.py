from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort


class CloseTaskUseCase:
    def __init__(self, task_repository: TaskRepositoryPort) -> None:
        self._task_repository = task_repository

    def execute(self, url: str) -> None:
        before = self._task_repository.all_tasks()
        after = []

        i = 0
        while before[i].url != url:
            after.append(before[i])
            i += 1

        i += 1
        while len(before) > i:
            after.append(before[i].to_new())
            i += 1

        self._task_repository.save(after)
