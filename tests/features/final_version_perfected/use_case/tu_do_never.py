import pytest

from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew, TaskLater, TaskNext, TaskNever
from ytreza_dev.features.final_version_perfected.use_case.do_later import DoLater
from ytreza_dev.features.final_version_perfected.use_case.do_never import DoNever


class TaskRepositoryForTest(TaskRepositoryPort):
    def __init__(self):
        self._tasks = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks

    def feed(self, tasks):
        self._tasks = tasks

@pytest.mark.parametrize("before, url, after", [
    [
        [
            TaskNew(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com")
        ],
        "https://url_2.com",
        [
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNever(title="buy the water", url="https://url_2.com")
        ]
    ],
    [
        [
            TaskNew(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com"),
            TaskNew(title="buy the bread", url="https://url_3.com")
        ],
        "https://url_3.com",
        [
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com"),
            TaskNever(title="buy the bread", url="https://url_3.com")
        ]
    ],
])
def test_do_later(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(tasks=before)

    DoNever(task_repository).execute(url=url)

    assert task_repository.all_tasks() == after
