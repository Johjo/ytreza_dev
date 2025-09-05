import pytest
from expression import Nothing

from tests.features.final_version_perfected.adapters import FvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import an_external_task, an_external_project, \
    a_fvp_task
from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformation
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ExternalTask, Project
from ytreza_dev.features.final_version_perfected.use_case.start_fvp_use_case import StartFvpUseCase


class TaskRepositoryForTest:
    def __init__(self):
        self._tasks = {}

    def all_tasks(self) -> dict[str, TaskInformation]:
        return self._tasks

    def save(self, task: TaskInformation) -> None:
        self._tasks[task.key] = task



class TodolistReaderForTest(TodolistReaderPort):
    def __init__(self) -> None:
        self._tasks : list[ExternalTask] = []

    def feed(self, tasks: list[ExternalTask]) -> None:
        self._tasks = tasks

    def all_tasks(self) -> list[ExternalTask]:
        return self._tasks


@pytest.fixture
def fvp_repository() -> FvpRepositoryForTest:
    return FvpRepositoryForTest()


@pytest.fixture
def todolist_reader() -> TodolistReaderForTest:
    return TodolistReaderForTest()


@pytest.fixture
def sut(todolist_reader: TodolistReaderForTest, fvp_repository: FvpRepositoryForTest,
        task_repository: TaskRepositoryForTest) -> StartFvpUseCase:
    return StartFvpUseCase(todolist_reader=todolist_reader, fvp_repository=fvp_repository, task_information_repository=task_repository)


def test_merge_no_task(fvp_repository: FvpRepositoryForTest, sut: StartFvpUseCase) -> None:
    sut.execute()
    assert fvp_repository.all_tasks() == []


def test_synchronize_task_in_fvp_repository(todolist_reader: TodolistReaderForTest,
                                            fvp_repository: FvpRepositoryForTest, sut: StartFvpUseCase) -> None:
    todolist_reader.feed([
        an_external_task(name="buy the milk", url="https://url_1.com", id="1",
                         project=an_external_project("1", "project 1")),
        an_external_task(name="buy the water", url="https://url_2.com", id="2",
                         project=an_external_project(key="2", name="project 2"))])

    sut.execute()

    assert fvp_repository.all_tasks() == [
        a_fvp_task("1").to_new(),
        a_fvp_task("2").to_new()]


@pytest.fixture
def task_repository() -> TaskRepositoryForTest:
    return TaskRepositoryForTest()


def test_synchronize_task_in_task_repository(todolist_reader: TodolistReaderForTest,
                                             task_repository: TaskRepositoryForTest,
                                             sut: StartFvpUseCase) -> None:
    todolist_reader.feed([
        an_external_task(name="buy the milk", url="https://url_1.com", id="1",
                         project=an_external_project("1", "project 1")),
        an_external_task(name="buy the water", url="https://url_2.com", id="2",
                         project=an_external_project(key="2", name="project 2"))])

    sut.execute()

    assert task_repository.all_tasks() == {
        "1": TaskInformation(
            key="1",
            title="buy the milk",
            project=Project(key="1", name="project 1"),
            url="https://url_1.com",
            due_date=Nothing
        ),
        "2": TaskInformation(
            key="2",
            title="buy the water",
            project=Project(key="2", name="project 2"),
            url="https://url_2.com",
            due_date=Nothing
        )}
