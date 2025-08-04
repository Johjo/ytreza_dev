from pyqure import Key # type: ignore

from ytreza_dev.features.start_fvp_use_case.use_case import TodolistReader, TaskRepository
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import TaskReader

TASK_READER_KEY = Key("task_reader", TaskReader)
TODOLIST_READER_KEY = Key("todolist reader", TodolistReader)
TASK_REPOSITORY_KEY = Key("task repository", TaskRepository)
