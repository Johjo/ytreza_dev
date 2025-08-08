from pathlib import Path

from ytreza_dev.features.final_version_perfected.types import TaskNew, TaskNext, TaskLater, TaskNever

from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.final_version_perfected.adapter.task_reader_from_json import TaskReaderFromJson


def test_read_data_from_json() -> None:
    # GIVEN
    json_path = Path("data_test/tasks.json")
    task_repository_from_json = TaskRepositoryFromJson(file_path=json_path)
    task_repository_from_json.save([
        TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
        TaskLater(title="buy the water", url="https://url_2.com", id="2"),
        TaskNew(title="buy the bread", url="https://url_3.com", id="3"),
        TaskNever(title="buy the butter", url="https://url_4.com", id="4"),

    ])

    # WHEN
    sut = TaskReaderFromJson(json_path)
    actual = sut.all_active_tasks()

    # THEN
    assert actual == [
        TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
        TaskLater(title="buy the water", url="https://url_2.com", id="2"),
        TaskNew(title="buy the bread", url="https://url_3.com", id="3"),
        TaskNever(title="buy the butter", url="https://url_4.com", id="4"),
    ]
