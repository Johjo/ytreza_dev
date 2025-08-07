from typing import Any

import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from tests.features.final_version_perfected.use_case.conftest import task_repository
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskBase, TaskNever
from ytreza_dev.features.final_version_perfected.use_case.close_task_use_case import CloseTaskUseCase


class ExternalTodolistForTest(ExternalTodolistPort):
    def __init__(self) -> None:
        self._history : list[dict[str, Any]]= []

    def history(self) -> list[dict[str, Any]]:
        return self._history

    def close_task(self, url: str) -> None:
        self._history.append({"action": "close", "url": url})


@pytest.fixture
def external_todolist() -> ExternalTodolistForTest:
    return ExternalTodolistForTest()


@pytest.fixture
def sut(task_repository: TaskRepositoryForTest, external_todolist: ExternalTodolistForTest) -> CloseTaskUseCase:
    return CloseTaskUseCase(task_repository=task_repository, external_todolist=external_todolist)


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
def test_remove_task_when_closed(before: list[TaskBase], url: str, after: list[TaskBase],
                                 task_repository: TaskRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after


def test_close_task_on_external_system(task_repository: TaskRepositoryForTest, sut: CloseTaskUseCase,
                                       external_todolist: ExternalTodolistForTest) -> None:
    task_repository.feed(tasks=[
        TaskNext(title="Buy the milk ", url="https://url_1.com"),
    ])
    sut.execute(url="https://url_1.com")
    assert external_todolist.history() == [{"action": "close", "url": "https://url_1.com"}]






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
def test_set_following_task_to_new(before: list[TaskBase], url: str, after: list[TaskBase], task_repository: TaskRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after


@pytest.mark.parametrize("before, url, after", [
    [
        [
            TaskNext(title="Buy the milk ", url="https://url_1.com"),
            TaskNever(title="Buy the water", url="https://url_2.com"),
            TaskNext(title="Buy the eggs", url="https://url_3.com"),
            TaskNever(title="Buy the bread", url="https://url_4.com"),
        ],
        "https://url_3.com",
        [
            TaskNext(title="Buy the milk ", url="https://url_1.com"),
            TaskNever(title="Buy the water", url="https://url_2.com"),
            TaskNever(title="Buy the bread", url="https://url_4.com"),
        ]
    ],
])
def test_never_task_stay_never(before: list[TaskBase], url: str, after: list[TaskBase], task_repository: TaskRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after



def test_when_only_never_all_go_new(task_repository: TaskRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=[TaskNext(title="Buy the milk ", url="https://url_1.com"),
                                TaskNever(title="Buy the water", url="https://url_2.com"),
                                TaskNever(title="Buy the eggs", url="https://url_3.com"),
                                TaskNever(title="Buy the bread", url="https://url_4.com")])

    sut.execute(url="https://url_1.com")
    assert task_repository.all_tasks() == [
                                TaskNew(title="Buy the water", url="https://url_2.com"),
                                TaskNew(title="Buy the eggs", url="https://url_3.com"),
                                TaskNew(title="Buy the bread", url="https://url_4.com")]
