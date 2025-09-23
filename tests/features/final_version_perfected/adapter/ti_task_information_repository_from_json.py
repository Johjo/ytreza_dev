import datetime
from pathlib import Path

import pytest
from approvaltests import verify
from expression import Nothing

from features.final_version_perfected.use_case.tu_do_partial import a_task
from ytreza_dev.features.final_version_perfected.adapter.task_information_repository_from_json import \
    TaskInformationRepositoryFromJson
from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformation
from ytreza_dev.features.final_version_perfected.types import Project


@pytest.mark.integration
def test_write_in_json() -> None:
    json_path = Path("./data_test/task_repository.json")
    sut = TaskInformationRepositoryFromJson(json_path)

    sut.save([
        a_task(key="1").to_information(),
        a_task(key="2", due_date=datetime.date(2017, 10, 27)).to_information(),
    ])

    verify(json_path.read_text(encoding="utf-8"))


@pytest.mark.integration
def test_read_from_json() -> None:
    json_path = Path("./data_test/task_repository.json")
    sut = TaskInformationRepositoryFromJson(json_path)

    expected_task : list[TaskInformation] = [
        a_task(key="1").to_information(),
        a_task(key="2", due_date=datetime.date(2017, 10, 27)).to_information(),
    ]
    sut.save(expected_task)

    assert sut.by_key(expected_task[0].key) == expected_task[0]
    assert sut.by_key(expected_task[1].key) == expected_task[1]
