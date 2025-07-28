import pytest

from ytreza_dev.features.start_fvp_use_case.use_case import Task, TaskRepository, TodolistReader, StartFvpUseCase


class TaskRepositoryForTest(TaskRepository):
    def __init__(self) -> None:
        self._tasks : list[Task] = []

    def all_tasks(self) -> list[Task]:
        return self._tasks

    def save(self, tasks: list[Task]) -> None:
        self._tasks = tasks


class TodolistReaderForTest(TodolistReader):
    def __init__(self) -> None:
        self._tasks : list[Task] = []

    def feed(self, tasks: list[Task]) -> None:
        self._tasks = tasks

    def all_tasks(self) -> list[Task]:
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
        Task(name="buy the milk", url="https://url_1.com"),
        Task(name="buy the water", url="https://url_2.com")])

    sut.execute()

    assert task_repository.all_tasks() == [
        Task(name="buy the milk", url="https://url_1.com"),
        Task(name="buy the water", url="https://url_2.com")]
