import datetime

import pytest

from features.final_version_perfected.use_case.tu_do_partial import a_task
from tests.features.final_version_perfected.adapters import FvpRepositoryForTest, TaskInformationRepositoryForTest
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
def fvp_repository() -> FvpRepositoryForTest:
    return FvpRepositoryForTest()


@pytest.fixture
def todolist_reader() -> TodolistReaderForTest:
    return TodolistReaderForTest()


@pytest.fixture
def task_information_repository() -> TaskInformationRepositoryForTest:
    return TaskInformationRepositoryForTest()

@pytest.fixture
def sut(todolist_reader: TodolistReaderForTest, fvp_repository: FvpRepositoryForTest,
        task_information_repository: TaskInformationRepositoryForTest) -> StartFvpUseCase:
    return StartFvpUseCase(todolist_reader=todolist_reader, fvp_repository=fvp_repository, task_information_repository=task_information_repository)


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


def test_synchronize_task_in_task_repository(todolist_reader: TodolistReaderForTest,
                                             task_information_repository: TaskInformationRepositoryForTest,
                                             sut: StartFvpUseCase) -> None:
    task_one = a_task(key="1")
    task_two = a_task(key="2", due_date=datetime.date(2017, 10, 27))

    todolist_reader.feed([
        task_one.to_external(),
        task_two.to_external(),
    ])

    sut.execute()

    assert task_information_repository.all_tasks() == {
        task_one.key: task_one.to_information(),
        task_two.key: task_two.to_information(),}
