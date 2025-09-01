import pytest

from tests.features.final_version_perfected.adapters import TaskFvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import an_external_task, an_external_project, \
    a_fvp_task
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ExternalTask
from ytreza_dev.features.final_version_perfected.use_case.start_fvp_use_case import StartFvpUseCase


class TodolistReaderForTest(TodolistReaderPort):
    def __init__(self) -> None:
        self._tasks : list[ExternalTask] = []

    def feed(self, tasks: list[ExternalTask]) -> None:
        self._tasks = tasks

    def all_tasks(self) -> list[ExternalTask]:
        return self._tasks


@pytest.fixture
def task_repository() -> TaskFvpRepositoryForTest:
    return TaskFvpRepositoryForTest()


@pytest.fixture
def todolist_reader() -> TodolistReaderForTest:
    return TodolistReaderForTest()


@pytest.fixture
def sut(todolist_reader: TodolistReaderForTest, task_repository: TaskFvpRepositoryForTest) -> StartFvpUseCase:
    return StartFvpUseCase(todolist_reader, task_repository)


def test_merge_no_task(task_repository: TaskFvpRepositoryForTest, sut: StartFvpUseCase) -> None:
    sut.execute()
    assert task_repository.all_tasks() == []


def test_synchronize_task_in_repository(todolist_reader: TodolistReaderForTest, task_repository: TaskFvpRepositoryForTest,
                                        sut: StartFvpUseCase) -> None:
    todolist_reader.feed([
        an_external_task(name="buy the milk", url="https://url_1.com", id="1",
                         project=an_external_project("1", "project 1")),
        an_external_task(name="buy the water", url="https://url_2.com", id="2",
                         project=an_external_project(key="2", name="project 2"))])

    sut.execute()

    assert task_repository.all_tasks() == [
        a_fvp_task("1").to_new(),
        a_fvp_task("2").to_new()]
