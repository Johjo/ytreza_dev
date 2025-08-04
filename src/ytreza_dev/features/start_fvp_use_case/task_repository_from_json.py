import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ytreza_dev.features.start_fvp_use_case.use_case import TaskRepository
from ytreza_dev.shared.final_version_perfected.types import TaskBase


class TaskRepositoryFromJson(TaskRepository):
    def all_tasks(self) -> list[TaskBase]:
        raise NotImplementedError()

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def save(self, tasks: list[TaskBase]) -> None:
        tasks_dict = [self._to_dict(task) for task in tasks]
        self._file_path.write_text(json.dumps(tasks_dict, indent=4))

    @staticmethod
    def _to_dict(task: TaskBase) -> dict[str, Any]:
        d = asdict(task)
        d.update({"status": "new"})
        return d
