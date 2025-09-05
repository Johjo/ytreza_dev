from typing import Any

import pytest

from tests.features.final_version_perfected.adapters import FvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_fvp_task
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
def sut(task_repository: FvpRepositoryForTest, external_todolist: ExternalTodolistForTest) -> CloseTaskUseCase:
    return CloseTaskUseCase(task_repository=task_repository, external_todolist=external_todolist)


@pytest.mark.parametrize("before, key, after", [
    [
        [a_fvp_task(key="1").to_next()],
        "1",
        []
    ],
    [
        [a_fvp_task(key="1").to_next(),
         a_fvp_task(key="2").to_next()],
        "2",
        [a_fvp_task(key="1").to_next()]
    ],
])
def test_remove_task_when_closed(before: list[TaskBase], key, after: list[TaskBase],
                                 task_repository: FvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(key=key)
    assert task_repository.all_tasks() == after




def test_close_task_on_external_system(task_repository: FvpRepositoryForTest, sut: CloseTaskUseCase,
                                       external_todolist: ExternalTodolistForTest) -> None:
    task_repository.feed(tasks=[
        a_fvp_task(key="1").to_next(),
        a_fvp_task(key="2").to_next(),
        a_fvp_task(key="3").to_later(),
    ])
    sut.execute(key="2")
    assert external_todolist.history() == [{"action": "close", "task_id": "2"}]

@pytest.mark.parametrize("before, key, after", [
    [
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_later(),
            a_fvp_task(key="3").to_next(),
            a_fvp_task(key="4").to_later(),
        ],
        "3",
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_later(),
            a_fvp_task("4").to_new(),
        ]
    ],
    [
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_later(),
            a_fvp_task(key="3").to_later(),
            a_fvp_task(key="4").to_later(),
        ],
        "1",
        [
            a_fvp_task("2").to_new(),
            a_fvp_task("3").to_new(),
            a_fvp_task("4").to_new(),
        ]
    ],
])
def test_set_following_task_to_new(before: list[TaskBase], key, after: list[TaskBase], task_repository: FvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(key=key)
    assert task_repository.all_tasks() == after


@pytest.mark.parametrize("before, url, after", [
    [
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_never(),
            a_fvp_task(key="3").to_next(),
            a_fvp_task(key="4").to_never(),
        ],
        "3",
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_never(),
            a_fvp_task(key="4").to_never(),
        ]
    ],
])
def test_never_task_stay_never(before: list[TaskBase], url: str, after: list[TaskBase], task_repository: FvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=before)
    sut.execute(key=url)
    assert task_repository.all_tasks() == after



def test_when_only_never_all_go_new(task_repository: FvpRepositoryForTest, sut: CloseTaskUseCase) -> None:
    task_repository.feed(tasks=[a_fvp_task(key="1").to_next(),
                                a_fvp_task(key="2").to_never(),
                                a_fvp_task(key="3").to_never(),
                                a_fvp_task(key="4").to_never()])

    sut.execute(key="1")

    assert task_repository.all_tasks() == [
        a_fvp_task("2").to_new(),
        a_fvp_task("3").to_new(),
        a_fvp_task("4").to_new()]
