import pytest

from ytreza_dev.features.todolist_query.todolist_query import TodolistReaderPort, Task, TodolistQuery


class TodolistReaderForTest(TodolistReaderPort):
    def __init__(self) -> None:
        self._all_tasks : list[Task] = []

    def all_tasks(self) -> list[Task]:
        return self._all_tasks

    def feed(self, tasks: list[Task]) -> None:
        self._all_tasks = tasks


@pytest.fixture
def todolist_reader() -> TodolistReaderForTest:
    return TodolistReaderForTest()

@pytest.fixture
def sut(todolist_reader: TodolistReaderForTest) -> TodolistQuery:
    return TodolistQuery(todolist_reader)


def test_list_nothing_when_no_task(sut: TodolistQuery) -> None:
    assert sut.all_tasks() == []


def test_list_tasks(sut: TodolistQuery, todolist_reader: TodolistReaderForTest) -> None:
    todolist_reader.feed([Task(name="buy the milk", url="https://url_1.com"), Task(name="buy the water", url="https://url_2.com")])

    all_tasks = sut.all_tasks()

    assert all_tasks == [Task(name="buy the milk", url="https://url_1.com"), Task(name="buy the water", url="https://url_2.com")]

