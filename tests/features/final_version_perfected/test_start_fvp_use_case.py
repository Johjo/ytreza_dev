import pytest

from ytreza_dev.features.final_version_perfected.use_case.start_fvp_use_case import StartFvpUseCase
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew, ExternalTask


class TaskRepositoryForTest(TaskRepositoryPort):
    def __init__(self) -> None:
        self._tasks : list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks


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
        ExternalTask(name="buy the milk", url="https://url_1.com"),
        ExternalTask(name="buy the water", url="https://url_2.com")])

    sut.execute()

    assert task_repository.all_tasks() == [
        TaskNew(title="buy the milk", url="https://url_1.com"),
        TaskNew(title="buy the water", url="https://url_2.com")]
