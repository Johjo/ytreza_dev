from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.shared.env_reader import EnvReaderPort
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


class ExternalTodolistFromTodoist(ExternalTodolistPort):
    def __init__(self, env_reader: EnvReaderPort) -> None:
        self._todoist = TodoistAPI(env_reader.read("TODOIST_API_TOKEN"))

    def close_task(self, url: str, task_id: str) -> None:
        print(f"close task {task_id} on {url}")
        self._todoist.close_task(task_id=task_id)
