from pathlib import Path

import pytest

from tests.features.final_version_perfected.fixtures import a_fvp_task
from ytreza_dev.features.final_version_perfected.adapter.task_fvp_reader_from_json import TaskFvpReaderFromJson
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import FvpRepositoryFromJson


@pytest.mark.integration
def test_read_data_from_json() -> None:
    # GIVEN
    json_path = Path("data_test/tasks.json")
    task_repository_from_json = FvpRepositoryFromJson(file_path=json_path)
    task_repository_from_json.save([
        a_fvp_task(key="1").to_next(),
        a_fvp_task(key="2").to_later(),
        a_fvp_task("3").to_new(),
        a_fvp_task(key="4").to_never(),

    ])

    # WHEN
    sut = TaskFvpReaderFromJson(json_path)
    actual = sut.all_active_tasks()

    # THEN
    assert actual == [
        a_fvp_task(key="1").to_next(),
        a_fvp_task(key="2").to_later(),
        a_fvp_task(key="3").to_new(),
        a_fvp_task(key="4").to_never(),
    ]