from approvaltests import verify # type: ignore
from pathlib import Path

from tests.features.final_version_perfected.fixtures import a_fvp_task
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import FvpRepositoryFromJson
from ytreza_dev.features.final_version_perfected.types import TaskBase


def test_write_in_json() -> None:
    json_path = Path("./data_test/tasks.json")
    sut = FvpRepositoryFromJson(json_path)

    sut.save([
        a_fvp_task("1").to_new(),
        a_fvp_task("2").to_new()])

    verify(json_path.read_text(encoding="utf-8"))


def test_read_from_json() -> None:
    json_path = Path("./data_test/tasks.json")
    sut = FvpRepositoryFromJson(json_path)

    expected_task : list[TaskBase] = [
        a_fvp_task(key="1").to_next(),
        a_fvp_task(key="2").to_later(),
        a_fvp_task("3").to_new(),
        a_fvp_task(key="4").to_never(),
    ]
    sut.save(expected_task)

    assert sut.all_tasks() == expected_task

