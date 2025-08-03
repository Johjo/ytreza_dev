import pytest

from ytreza_dev.features.start_fvp_use_case.use_case import TaskRepository
from ytreza_dev.shared.final_version_perfected.types import TaskNew, TaskLater, TaskNext, TaskBase


class TaskRepositoryForTest(TaskRepository):
    def __init__(self) -> None:
        self._tasks: list[TaskNew | TaskLater | TaskNext] = []

    def feed(self, tasks: list[TaskNew | TaskLater | TaskNext]):
        self._tasks = tasks

    def all_tasks(self):
        return self._tasks

    def save(self, tasks: list[TaskNew | TaskLater | TaskNext]) -> None:
        self._tasks = tasks


class ChooseTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self._task_repository = task_repository

    def execute(self, url: str):
        all_tasks_before = self._task_repository.all_tasks()
        all_tasks_after = []

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

    def _first_new_index(self, all_tasks_before):
        i = 1

        for index, task in enumerate(all_tasks_before):
            if isinstance(task, TaskNew):
                return index



def test_repository():
    task_repository = TaskRepositoryForTest()
    task_repository.feed([TaskNew(title="buy the milk", url="https://url_1.com"),
                          TaskNew(title="buy the water", url="https://url_2.com")])

    assert task_repository.all_tasks() == [TaskNew(title="buy the milk", url="https://url_1.com"),
                                           TaskNew(title="buy the water", url="https://url_2.com")]


@pytest.mark.parametrize("initial_tasks, chosen_url, expected", [
    [[TaskNew(title="buy the milk", url="https://url_1.com"),
      TaskNew(title="buy the water", url="https://url_2.com")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com")]],

    [[TaskNew(title="buy the milk", url="https://url_1.com"),
      TaskNew(title="buy the water", url="https://url_2.com")],
     "https://url_2.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNext(title="buy the water", url="https://url_2.com")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNext(title="buy the water", url="https://url_2.com"),
      TaskNew(title="buy the eggs", url="https://url_3.com")],
     "https://url_2.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNext(title="buy the water", url="https://url_2.com"),
      TaskLater(title="buy the eggs", url="https://url_3.com")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskNew(title="buy the eggs", url="https://url_3.com")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskLater(title="buy the eggs", url="https://url_3.com")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskNew(title="buy the eggs", url="https://url_3.com")],
     "https://url_3.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskNext(title="buy the eggs", url="https://url_3.com")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNew(title="buy the water", url="https://url_2.com"),
      TaskNew(title="buy the eggs", url="https://url_3.com")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskNew(title="buy the eggs", url="https://url_3.com")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskLater(title="buy the eggs", url="https://url_3.com"),
      TaskNew(title="buy the bread", url="https://url_4.com")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskLater(title="buy the water", url="https://url_2.com"),
      TaskLater(title="buy the eggs", url="https://url_3.com"),
      TaskLater(title="buy the bread", url="https://url_4.com")]],


    [[TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNext(title="buy the water", url="https://url_2.com"),
      TaskNext(title="buy the eggs", url="https://url_3.com"),
      TaskNew(title="buy the bread", url="https://url_4.com")],
     "https://url_4.com",
     [TaskNext(title="buy the milk", url="https://url_1.com"),
      TaskNext(title="buy the water", url="https://url_2.com"),
      TaskNext(title="buy the eggs", url="https://url_3.com"),
      TaskNext(title="buy the bread", url="https://url_4.com")]],
])
def test_xxx(initial_tasks, chosen_url, expected):
    task_repository = TaskRepositoryForTest()
    task_repository.feed(initial_tasks)
    sut = ChooseTaskUseCase(task_repository)

    sut.execute(url=chosen_url)

    assert task_repository.all_tasks() == expected
