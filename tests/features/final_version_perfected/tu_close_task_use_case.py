import pytest

from tests.features.final_version_perfected.test_choose_task_use_case import TaskRepositoryForTest
from ytreza_dev.features.final_version_perfected.use_case.close_task_use_case import CloseTaskUseCase
from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskBase


@pytest.mark.parametrize("before, url, after", [
    [
        [TaskNext(title="Buy the milk ", url="https://url_1.com")],
        "https://url_1.com",
        []
    ],
    [
        [TaskNext(title="Buy the milk ", url="https://url_1.com"),
         TaskNext(title="Buy the water", url="https://url_2.com")],
        "https://url_2.com",
        [TaskNext(title="Buy the milk ", url="https://url_1.com")]
    ],
])
def test_remove_task_when_closed(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(tasks=before)
    sut = CloseTaskUseCase(task_repository)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after


@pytest.mark.parametrize("before, url, after", [
    [
        [
            TaskNext(title="Buy the milk ", url="https://url_1.com"),
            TaskLater(title="Buy the water", url="https://url_2.com"),
            TaskNext(title="Buy the eggs", url="https://url_3.com"),
            TaskLater(title="Buy the bread", url="https://url_4.com"),
        ],
        "https://url_3.com",
        [
            TaskNext(title="Buy the milk ", url="https://url_1.com"),
            TaskLater(title="Buy the water", url="https://url_2.com"),
            TaskNew(title="Buy the bread", url="https://url_4.com"),
        ]
    ],
    [
        [
            TaskNext(title="Buy the milk ", url="https://url_1.com"),
            TaskLater(title="Buy the water", url="https://url_2.com"),
            TaskLater(title="Buy the eggs", url="https://url_3.com"),
            TaskLater(title="Buy the bread", url="https://url_4.com"),
        ],
        "https://url_1.com",
        [
            TaskNew(title="Buy the water", url="https://url_2.com"),
            TaskNew(title="Buy the eggs", url="https://url_3.com"),
            TaskNew(title="Buy the bread", url="https://url_4.com"),
        ]
    ],
])
def test_set_following_task_to_new(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(tasks=before)
    sut = CloseTaskUseCase(task_repository)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after
