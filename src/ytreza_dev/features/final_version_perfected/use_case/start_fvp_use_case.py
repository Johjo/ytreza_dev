from expression import Nothing

from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformationRepositoryPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.port.task_repository import FvpRepositoryPort
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import TaskNew, ExternalTask, ExternalProject, Project


class StartFvpUseCase:
    def __init__(self, todolist_reader: TodolistReaderPort, fvp_repository: FvpRepositoryPort, task_information_repository: TaskInformationRepositoryPort) -> None:
        self._task_information_repository = task_information_repository
        self._todolist_reader = todolist_reader
        self._fvp_repository = fvp_repository

    def execute(self) -> None:

        all_external_tasks : list[ExternalTask] = self._todolist_reader.all_tasks()
        self._fvp_repository.save([self._to_task_new(task) for task in all_external_tasks])
        self._task_information_repository.save([self._to_task_information(task) for task in all_external_tasks])

    @staticmethod
    def _to_task_information(external_task: ExternalTask) -> TaskInformation:
        return TaskInformation(
            key=external_task.id,
            title=external_task.name,
            project=Project(key=external_task.project.key, name=external_task.project.name),
            url=external_task.url,
            due_date=Nothing
        )

    @staticmethod
    def _to_task_new(task: ExternalTask) -> TaskNew :
        return TaskNew(id=task.id)

    @staticmethod
    def _to_project(project: ExternalProject) -> Project:
        return Project(key=project.key, name=project.name)
