import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_task_new, an_external_task
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
def task_repository() -> TaskRepositoryForTest:
    return TaskRepositoryForTest()


@pytest.fixture
def todolist_reader() -> TodolistReaderForTest:
    return TodolistReaderForTest()


@pytest.fixture
def sut(todolist_reader: TodolistReaderForTest, task_repository: TaskRepositoryForTest) -> StartFvpUseCase:
    return StartFvpUseCase(todolist_reader, task_repository)


def test_merge_no_task(task_repository: TaskRepositoryForTest, sut: StartFvpUseCase) -> None:
    sut.execute()
    assert task_repository.all_tasks() == []


def test_synchronize_task_in_repository(todolist_reader: TodolistReaderForTest, task_repository: TaskRepositoryForTest,
                                        sut: StartFvpUseCase) -> None:
    todolist_reader.feed([
        an_external_task(name="buy the milk", url="https://url_1.com", id="1"),
        ExternalTask(name="buy the water", url="https://url_2.com", id="2")])

    sut.execute()

    assert task_repository.all_tasks() == [
        a_task_new(title="buy the milk", url="https://url_1.com", id="1"),
        a_task_new(title="buy the water", url="https://url_2.com", id="2")]
