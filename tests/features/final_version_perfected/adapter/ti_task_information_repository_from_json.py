from pathlib import Path

import pytest
from approvaltests import verify
from expression import Nothing

from ytreza_dev.features.final_version_perfected.adapter.task_information_repository_from_json import \
    TaskInformationRepositoryFromJson
from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformation
from ytreza_dev.features.final_version_perfected.types import Project


@pytest.mark.integration
def test_write_in_json() -> None:
    json_path = Path("./data_test/task_repository.json")
    sut = TaskInformationRepositoryFromJson(json_path)

    sut.save([
        TaskInformation(key="1", title="buy the milk", project=Project(key="1", name="Project 1"), due_date=Nothing, url="https://url_1.com"),
        TaskInformation(key="2", title="buy the water", project=Project(key="2", name="Project 2"), due_date=Nothing, url="https://url_2.com"),
    ])

    verify(json_path.read_text(encoding="utf-8"))


@pytest.mark.integration
def test_read_from_json() -> None:
    json_path = Path("./data_test/task_repository.json")
    sut = TaskInformationRepositoryFromJson(json_path)

    expected_task : list[TaskInformation] = [
        TaskInformation(key="1", title="buy the milk", project=Project(key="1", name="Project 1"), due_date=Nothing, url="https://url_1.com"),
        TaskInformation(key="2", title="buy the water", project=Project(key="2", name="Project 2"), due_date=Nothing, url="https://url_2.com"),
    ]
    sut.save(expected_task)

    assert sut.by_key(expected_task[0].key) == expected_task[0]
    assert sut.by_key(expected_task[1].key) == expected_task[1]
