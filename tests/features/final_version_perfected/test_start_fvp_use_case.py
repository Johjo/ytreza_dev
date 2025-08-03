import pytest

from ytreza_dev.features.start_fvp_use_case.use_case import OldTask, TaskRepository, TodolistReader, StartFvpUseCase, \
    ExternalTask
from ytreza_dev.shared.final_version_perfected.types import TaskBase, TaskNew


class TaskRepositoryForTest(TaskRepository):
    def __init__(self) -> None:
        self._tasks : list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks


class TodolistReaderForTest(TodolistReader):
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
