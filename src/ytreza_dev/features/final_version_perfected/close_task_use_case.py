from ytreza_dev.features.start_fvp_use_case.use_case import TaskRepository


class CloseTaskUseCase:
    def __init__(self, task_repository: TaskRepository) -> None:
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
