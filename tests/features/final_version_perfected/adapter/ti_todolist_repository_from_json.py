from approvaltests import verify # type: ignore
from pathlib import Path

from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.final_version_perfected.types import TaskNew, TaskNext, TaskLater, TaskBase, TaskNever


def test_write_in_json() -> None:
    json_path = Path("./data_test/tasks.json")
    sut = TaskRepositoryFromJson(json_path)

    sut.save([
        TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
        TaskNew(title="buy the water", url="https://url_2.com", id="2")])

    verify(json_path.read_text(encoding="utf-8"))


def test_read_from_json() -> None:
    json_path = Path("./data_test/tasks.json")
    sut = TaskRepositoryFromJson(json_path)

    expected_task : list[TaskBase] = [
        TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
        TaskLater(title="buy the water", url="https://url_2.com", id="2"),
        TaskNew(title="buy the bread", url="https://url_3.com", id="3"),
        TaskNever(title="buy the butter", url="https://url_4.com", id="4"),
    ]
    sut.save(expected_task)

    assert sut.all_tasks() == expected_task

