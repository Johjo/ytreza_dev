from approvaltests import verify
from pathlib import Path

from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.start_fvp_use_case.use_case import Task


def test_write_in_json():
    json_path = Path("./data_test/tasks.json")
    sut = TaskRepositoryFromJson(json_path)

    sut.save([
        Task(name="buy the milk", url="https://url_1.com"),
        Task(name="buy the water", url="https://url_2.com")])

    verify(Path("tasks.json").read_text(encoding="utf-8"))

