from pyqure import Key # type: ignore

from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformationRepositoryPort
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.port.task_repository import FvpRepositoryPort
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort

TASK_FVP_READER_KEY = Key("task fvp reader", TaskFvpReaderPort)
FVP_REPOSITORY_KEY = Key("fvp repository", FvpRepositoryPort)
TODOLIST_READER_KEY = Key("todolist reader", TodolistReaderPort)
EXTERNAL_TODOLIST_KEY = Key("external todolist", ExternalTodolistPort)
TASK_INFORMATION_REPOSITORY_KEY = Key("task information repository", TaskInformationRepositoryPort)

