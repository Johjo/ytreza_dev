from approvaltests import verify  # type: ignore

from ytreza_dev.features.final_version_perfected.adapter.external_todolist_from_todoist import \
    ExternalTodolistFromTodoist
from ytreza_dev.shared.env_reader import EnvReaderFromEnv
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


def test_close_task() -> None:
    env_reader = EnvReaderFromEnv(env_path=".env.test")
    todoist = TodoistAPI(env_reader.read("TODOIST_API_TOKEN"))
    task_id = todoist.open_task(content="buy the milk")

    sut = ExternalTodolistFromTodoist(env_reader=env_reader)
    sut.close_task(url="", task_id=task_id)

    tasks = todoist.get_all_tasks()
    verify("\n".join([str(task) for task in tasks]), encoding="utf-8")
