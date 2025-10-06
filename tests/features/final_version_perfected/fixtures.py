import datetime
from dataclasses import dataclass

from expression import Nothing, Some, Option

from ytreza_dev.features.final_version_perfected.port.task_information_repository import TaskInformation
from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskNever, ExternalTask, \
    ExternalProject, Project, TaskBase


def a_project(key:str, name:str)-> Project:
    return Project(key=key, name=name)


@dataclass(frozen=True, eq=True)
class FvpTaskBuilder:
    key: str

    def to_new(self) -> TaskNew:
        return TaskNew(id=self.key)

    def to_never(self) -> TaskNever:
        return TaskNever(id=self.key)

    def to_next(self) -> TaskNext:
        return TaskNext(id=self.key)

    def to_later(self) -> TaskLater:
        return TaskLater(id=self.key)


def a_fvp_task(key: str) -> FvpTaskBuilder:
    return FvpTaskBuilder(key=key)


def an_external_project(key: str, name: str):
    return ExternalProject(name=name, key=key)


class ExternalTaskBuilder:
    pass


def an_external_task(name: str, url: str, id: str,
                     project: ExternalProject = ExternalProject(name="Project", key="1")) -> ExternalTask:
    return ExternalTask(name=name, url=url, id=id, project=project, due_date=Nothing)


class TaskBuilder:
    def __init__(self, key: str, url: str | None = None, title: str | None = None, project: Project | None = None, due_date: datetime.date | None = None) -> None:
        self.key = key
        self._url = Some(url) if url else Nothing
        self._title = Some(title) if title else Nothing
        self._project : Option[Project] = Some(project) if project else Nothing
        self._due_date = Some(due_date) if due_date else Nothing

    @property
    def title(self) -> str:
        return self._title.default_value(f"Do task {self.key}")

    @property
    def url(self) -> str:
        return self._url.default_value(f"https://url_{self.key}.com")

    @property
    def project(self) -> Project:
        return self._project.default_value(Project(key=self.key, name=f"Project {self.key}"))

    @property
    def due_date(self) -> Option[datetime.date]:
        return self._due_date

    def to_new(self) -> TaskNew:
        return self._task_base().to_new()

    def to_next(self) -> TaskNext:
        return self._task_base().to_next()

    def to_later(self) -> TaskLater:
        return self._task_base().to_later()

    def to_never(self) -> TaskNever:
        return self._task_base().to_never()

    def to_information(self) -> TaskInformation:
        return TaskInformation(key=self.key, title=self.title, project=self.project, due_date=self.due_date, url=self.url)

    def _task_base(self) -> TaskBase:
        return TaskBase(id=self.key)

    def to_external(self) -> ExternalTask:
        return ExternalTask(id=self.key, name=self.title, project=self.project, url=self.url, due_date=self.due_date)


class ProjectBuilder:
    def __init__(self, key: str):
        self._key = key

    def to_project(self) -> Project:
        return Project(key=self._key, name=f"Project {self._key}")
