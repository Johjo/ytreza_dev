from approvaltests import verify  # type: ignore

from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.shared.env_reader import EnvReaderFromEnv, EnvReaderPort
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


class ExternalTodolistFromTodoist(ExternalTodolistPort):
    def __init__(self, env_reader: EnvReaderPort) -> None:
        self._todoist = TodoistAPI(env_reader.read("TODOIST_API_TOKEN"))

    def close_task(self, url: str, task_id: str) -> None:
        self._todoist.close_task(task_id=task_id)


def test_close_task() -> None:
    env_reader = EnvReaderFromEnv(env_path=".env.test")
    todoist = TodoistAPI(env_reader.read("TODOIST_API_TOKEN"))
    task_id = todoist.open_task(content="buy the milk")

    sut = ExternalTodolistFromTodoist(env_reader=env_reader)
    sut.close_task(url="", task_id=task_id)

    tasks = todoist.get_all_tasks()
    verify("\n".join([str(task) for task in tasks]), encoding="utf-8")
