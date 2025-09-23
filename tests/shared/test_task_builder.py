import datetime

import pytest
from expression import Nothing, Some

from features.final_version_perfected.fixtures import TaskBuilder
from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformation
from ytreza_dev.features.final_version_perfected.types import Project, ExternalTask


@pytest.mark.parametrize("key, expected", [
    ["1", TaskInformation(key="1", url="https://url_1.com", title="Do task 1", due_date=Nothing,
                          project=Project(key="1", name="Project 1"))],
    ["2", TaskInformation(key="2", url="https://url_2.com", title="Do task 2", due_date=Nothing,
                          project=Project(key="2", name="Project 2"))],
])
def test_default_task_information(key: str, expected: TaskInformation) -> None:
    builder = TaskBuilder(key=key)

    assert builder.to_information() == expected


def test_task_information_with_value():
    builder = TaskBuilder(key="1",
                          url="https://another_url.com",
                          title="Another title",
                          project=Project(key="xxx", name="Another project"), due_date=datetime.date(2013, 11, 17))

    assert builder.to_information() == TaskInformation(key="1",
                                                       url="https://another_url.com",
                                                       title="Another title",
                                                       due_date=Some(datetime.date(2013, 11, 17)),
                                                       project=Project(key="xxx", name="Another project"))


@pytest.mark.parametrize("key, expected", [
    ["1", ExternalTask(id="1", url="https://url_1.com", name="Do task 1", due_date=Nothing,
                       project=Project(key="1", name="Project 1"))],
    ["2", ExternalTask(id="2", url="https://url_2.com", name="Do task 2", due_date=Nothing,
                       project=Project(key="2", name="Project 2"))],
])
def test_default_task_information(key: str, expected: TaskInformation) -> None:
    builder = TaskBuilder(key=key)

    assert builder.to_external() == expected
