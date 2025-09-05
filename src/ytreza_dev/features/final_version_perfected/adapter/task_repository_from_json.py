import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from ytreza_dev.features.final_version_perfected.port.task_repository import FvpRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew, TaskNext, TaskLater, TaskNever


class FvpRepositoryFromJson(FvpRepositoryPort):
    def all_tasks(self) -> list[TaskBase]:

        tasks = json.loads(self._file_path.read_text())
        return [self.to_task_base(task) for task in tasks]

    @staticmethod
    def to_task_base(task: dict[str, str]) -> TaskBase:
        match task["status"]:
            case "new":
                return TaskNew(id=task["id"])
            case "next":
                return TaskNext(id=task["id"])
            case "later":
                return TaskLater(id=task["id"])
            case "never":
                return TaskNever(id=task["id"])
        raise ValueError(f"Unknown status: {task['status']}")

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path

    def save(self, tasks: list[TaskBase]) -> None:
        tasks_dict = [self._to_dict(task) for task in tasks]
        self._file_path.write_text(json.dumps(tasks_dict, indent=4))

    @staticmethod
    def _to_dict(task: TaskBase) -> dict[str, Any]:
        d = asdict(task)
        match task:
            case TaskNext():
                d.update({"status": "next"})
            case TaskNew():
                d.update({"status": "new"})
            case TaskLater():
                d.update({"status": "later"})
            case TaskNever():
                d.update({"status": "never"})

        return d