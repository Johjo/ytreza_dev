import datetime
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from expression import Nothing, Some

from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformationRepositoryPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.types import Project


class TaskInformationRepositoryFromJson(TaskInformationRepositoryPort):
    def __init__(self, json_path: Path) -> None:
        self._json_path = json_path


    def save(self, tasks: list[TaskInformation]) -> None:
        tasks_dict = [self._to_dict(task) for task in tasks]
        self._json_path.write_text(json.dumps(tasks_dict, indent=4))

    @staticmethod
    def _to_dict(task: TaskInformation) -> dict[str, Any]:
        d = {
            "key": task.key,
            "title": task.title,
            "project": asdict(task.project),
            "url": task.url,
        }

        due_date = task.due_date.default_value(None)

        if due_date:
            d.update({"due_date": due_date.isoformat()})

        return d

    def by_key(self, key: str) -> TaskInformation:
        tasks = json.loads(self._json_path.read_text(encoding="utf-8"))
        return [self._to_task_information(task) for task in tasks if task["key"] == key][0]

    @staticmethod
    def _to_task_information(task) -> TaskInformation:
        return TaskInformation(
            key=task["key"],
            title=task["title"],
            project=Project(key=task["project"]["key"], name=task["project"]["name"]),
            url=task["url"],
            due_date= Some(datetime.date.fromisoformat(task["due_date"])) if "due_date" in task else Nothing
        )
