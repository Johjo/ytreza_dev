from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformationReaderPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.types import Project
from ytreza_dev.shared.env_reader import EnvReaderFromEnv
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI, TodoistTask


class TaskInformationReaderFromTodoist(TaskInformationReaderPort):
    def __init__(self, env_reader: EnvReaderFromEnv) -> None:
        self._todoist = TodoistAPI(env_reader.read("TODOIST_API_TOKEN"))

    def by_key(self, key: str) -> TaskInformation:
        task : TodoistTask = self._todoist.task_by_id(task_id=key)
        return TaskInformation(key=task.id, title=task.name, project=Project(key=task.project.id, name=task.project.name), due_date=None)
