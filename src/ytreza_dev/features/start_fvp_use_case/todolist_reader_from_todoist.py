from ytreza_dev.features.start_fvp_use_case.use_case import TodolistReader, Task
from ytreza_dev.shared.env_reader import EnvReaderPort
from ytreza_dev.shared.todoist.todoist_api import TodoistAPI


class TodolistReaderFromTodoist(TodolistReader):
    def __init__(self, env_reader: EnvReaderPort):
        self._env_reader = EnvReaderPort()

    def all_tasks(self) -> list[Task]:
        todoist = TodoistAPI(self._env_reader.read("TODOIST_API_TOKEN"))
        tasks = todoist.get_all_tasks()
        return [Task(name=task.name, url=task.url) for task in tasks]
