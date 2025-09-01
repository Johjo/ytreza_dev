from typing import Any

import pytest

from tests.features.final_version_perfected.adapters import TaskFvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_task_next, a_task_later, a_task_new, a_task_never
from tests.features.final_version_perfected.use_case.conftest import task_repository
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.types import TaskBase
from ytreza_dev.features.final_version_perfected.use_case.close_task_use_case import CloseTaskUseCase


class ExternalTodolistForTest(ExternalTodolistPort):
    def __init__(self) -> None:
        self._history : list[dict[str, Any]]= []

    def history(self) -> list[dict[str, Any]]:
        return self._history

    def close_task(self, url: str, task_id: str) -> None:
        self._history.append({"action": "close", "task_id": task_id})


@pytest.fixture
def external_todolist() -> ExternalTodolistForTest:
    return ExternalTodolistForTest()


@pytest.fixture
def sut(task_repository: TaskFvpRepositoryForTest, external_todolist: ExternalTodolistForTest) -> CloseTaskUseCase:
    return CloseTaskUseCase(task_repository=task_repository, external_todolist=external_todolist)


@pytest.mark.parametrize("before, url, after", [
    [
        [a_task_next(title="Buy the milk ", url="https://url_1.com", id="1")],
        "https://url_1.com",
        []
    ],
    [
        [a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
         a_task_next(title="Buy the water", url="https://url_2.com", id="2")],
        "https://url_2.com",
        [a_task_next(title="Buy the milk ", url="https://url_1.com", id="1")]
    ],
])
def test_remove_task_when_closed(before: list[TaskBase], url: str, after: list[TaskBase],
                                 task_repository: TaskFvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after




def test_close_task_on_external_system(task_repository: TaskFvpRepositoryForTest, sut: CloseTaskUseCase,
                                       external_todolist: ExternalTodolistForTest) -> None:
    task_repository.feed(tasks=[
        a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
        a_task_next(title="Buy the milk ", url="https://url_2.com", id="2"),
        a_task_later(title="Buy the milk ", url="https://url_3.com", id="3"),
    ])
    sut.execute(url="https://url_2.com")
    assert external_todolist.history() == [{"action": "close", "task_id": "2"}]






@pytest.mark.parametrize("before, url, after", [
    [
        [
            a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
            a_task_later(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_next(title="Buy the eggs", url="https://url_3.com", id="3"),
            a_task_later(title="Buy the bread", url="https://url_4.com", id="4"),
        ],
        "https://url_3.com",
        [
            a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
            a_task_later(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_new(title="Buy the bread", url="https://url_4.com", id="4"),
        ]
    ],
    [
        [
            a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
            a_task_later(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_later(title="Buy the eggs", url="https://url_3.com", id="3"),
            a_task_later(title="Buy the bread", url="https://url_4.com", id="4"),
        ],
        "https://url_1.com",
        [
            a_task_new(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_new(title="Buy the eggs", url="https://url_3.com", id="3"),
            a_task_new(title="Buy the bread", url="https://url_4.com", id="4"),
        ]
    ],
])
def test_set_following_task_to_new(before: list[TaskBase], url: str, after: list[TaskBase], task_repository: TaskFvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after


@pytest.mark.parametrize("before, url, after", [
    [
        [
            a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
            a_task_never(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_next(title="Buy the eggs", url="https://url_3.com", id="3"),
            a_task_never(title="Buy the bread", url="https://url_4.com", id="4"),
        ],
        "https://url_3.com",
        [
            a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
            a_task_never(title="Buy the water", url="https://url_2.com", id="2"),
            a_task_never(title="Buy the bread", url="https://url_4.com", id="4"),
        ]
    ],
])
def test_never_task_stay_never(before: list[TaskBase], url: str, after: list[TaskBase], task_repository: TaskFvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(url=url)
    assert task_repository.all_tasks() == after



def test_when_only_never_all_go_new(task_repository: TaskFvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=[a_task_next(title="Buy the milk ", url="https://url_1.com", id="1"),
                                a_task_never(title="Buy the water", url="https://url_2.com", id="2"),
                                a_task_never(title="Buy the eggs", url="https://url_3.com", id="3"),
                                a_task_never(title="Buy the bread", url="https://url_4.com", id="4")])

    sut.execute(url="https://url_1.com")
    assert task_repository.all_tasks() == [
                                a_task_new(title="Buy the water", url="https://url_2.com", id="2"),
                                a_task_new(title="Buy the eggs", url="https://url_3.com", id="3"),
                                a_task_new(title="Buy the bread", url="https://url_4.com", id="4")]
