import pytest

from ytreza_dev.features.todolist_query.todoist_adapter import TodolistReaderFromTodoist
from ytreza_dev.features.todolist_query.todolist_query import Task

@pytest.fixture
def adapter() -> TodolistReaderFromTodoist:
    return TodolistReaderFromTodoist()


def test_todoist_adapter_can_fetch_tasks(adapter: TodolistReaderFromTodoist):
    all_tasks = adapter.all_tasks()

    assert isinstance(all_tasks, list)

    assert all(isinstance(task, Task) for task in all_tasks)

