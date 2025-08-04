from approvaltests import verify # type: ignore
from pathlib import Path

from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.shared.final_version_perfected.types import TaskNew


def test_write_in_json() -> None:
    json_path = Path("./data_test/tasks.json")
    sut = TaskRepositoryFromJson(json_path)

    sut.save([
        TaskNew(title="buy the milk", url="https://url_1.com"),
        TaskNew(title="buy the water", url="https://url_2.com")])

    verify(json_path.read_text(encoding="utf-8"))

