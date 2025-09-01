from pathlib import Path


from tests.features.final_version_perfected.fixtures import a_task_next, a_task_later, a_task_new, a_task_never
from ytreza_dev.features.final_version_perfected.adapter.task_fvp_reader_from_json import TaskFvpReaderFromJson
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskFvpRepositoryFromJson


def test_read_data_from_json() -> None:
    # GIVEN
    json_path = Path("data_test/tasks.json")
    task_repository_from_json = TaskFvpRepositoryFromJson(file_path=json_path)
    task_repository_from_json.save([
        a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
        a_task_later(title="buy the water", url="https://url_2.com", id="2"),
        a_task_new(title="buy the bread", url="https://url_3.com", id="3"),
        a_task_never(title="buy the butter", url="https://url_4.com", id="4"),

    ])

    # WHEN
    sut = TaskFvpReaderFromJson(json_path)
    actual = sut.all_active_tasks()

    # THEN
    assert actual == [
        a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
        a_task_later(title="buy the water", url="https://url_2.com", id="2"),
        a_task_new(title="buy the bread", url="https://url_3.com", id="3"),
        a_task_never(title="buy the butter", url="https://url_4.com", id="4"),
    ]