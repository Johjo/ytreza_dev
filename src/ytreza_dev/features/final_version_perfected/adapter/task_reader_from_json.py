import json
from pathlib import Path

from ytreza_dev.features.final_version_perfected.port.task_reader import TaskReader
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew, TaskNext, TaskLater, TaskNever, Project


class TaskReaderFromJson(TaskReader):
    def __init__(self, json_path: Path) -> None:
        self._json_path = json_path

    def all_active_tasks(self) -> list[TaskBase]:
        tasks = json.loads(self._json_path.read_text(encoding="utf-8"))
        return [self._to_task(task) for task in tasks]

    def _to_task(self, task: dict[str, str]) -> TaskBase:
        match task["status"]:
            case "new":
                return TaskNew(title=task["title"], url=task["url"], id=task["id"], project=self._to_project(task))
            case "next":
                return TaskNext(title=task["title"], url=task["url"], id=task["id"], project=self._to_project(task))
            case "later":
                return TaskLater(title=task["title"], url=task["url"], id=task["id"], project=self._to_project(task))
            case "never":
                return TaskNever(title=task["title"], url=task["url"], id=task["id"], project=self._to_project(task))
        raise ValueError(f"Unknown status: {task['status']}")

    @staticmethod
    def _to_project(task) -> Project:
        return Project(key=task["project"]["key"], name=task["project"]["name"])

