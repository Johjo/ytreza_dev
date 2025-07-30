import json
from pathlib import Path

from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.start_fvp_use_case.use_case import Task
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import TaskReader
from ytreza_dev.features.todolist_query_fvp.task_reader_from_json import TaskReaderFromJson
from ytreza_dev.features.todolist_query_fvp.types import TaskBase, TaskNew


def test_read_data_from_json_when_created():
    # GIVEN
    json_path = Path("data_test/tasks.json")
    task_repository_from_json = TaskRepositoryFromJson(file_path=json_path)
    task_repository_from_json.save([
        Task(name="buy the milk", url="https://url_1.com"),
        Task(name="buy the water", url="https://url_2.com")])

    # WHEN
    sut = TaskReaderFromJson(json_path)
    actual = sut.all_active_tasks()

    # THEN
    assert actual == [TaskNew(title="buy the milk", url="https://url_1.com"), TaskNew(title="buy the water", url="https://url_2.com")]
