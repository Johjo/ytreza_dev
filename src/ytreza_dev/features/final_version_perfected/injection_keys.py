from pyqure import Key # type: ignore

from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformationReaderPort
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort

TASK_FVP_READER_KEY = Key("task fvp reader", TaskFvpReaderPort)
TODOLIST_READER_KEY = Key("todolist reader", TodolistReaderPort)
TASK_REPOSITORY_KEY = Key("task repository", TaskRepositoryPort)
EXTERNAL_TODOLIST_KEY = Key("external todolist", ExternalTodolistPort)
TASK_INFORMATION_READER_KEY = Key("task  information reader", TaskInformationReaderPort)
