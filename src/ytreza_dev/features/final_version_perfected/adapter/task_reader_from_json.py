import json
from pathlib import Path

from ytreza_dev.features.final_version_perfected.port.task_reader import TaskReader
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew


class TaskReaderFromJson(TaskReader):
    def __init__(self, json_path: Path) -> None:
        self._json_path = json_path

    def all_active_tasks(self) -> list[TaskBase]:
        tasks = json.loads(self._json_path.read_text(encoding="utf-8"))
        return [TaskNew(title=task["title"], url=task["url"]) for task in tasks]