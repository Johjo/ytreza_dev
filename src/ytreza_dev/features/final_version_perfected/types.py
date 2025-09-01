import datetime
from dataclasses import dataclass
from typing import Tuple

from expression import Option


@dataclass(frozen=True, eq=True)
class TaskDetail:
    title: str
    url: str
    project_name: str
    due_date: Option[datetime.date]


@dataclass(frozen=True, eq=True)
class NothingToDo:
    pass


@dataclass(frozen=True, eq=True)
class DoTheTask:
    task: TaskDetail


@dataclass(frozen=True, eq=True)
class ChooseTaskBetween:
    tasks: Tuple[TaskDetail, TaskDetail]


NextAction = NothingToDo | DoTheTask | ChooseTaskBetween

@dataclass(frozen=True, eq=True)
class Project:
    key: str
    name: str


@dataclass(frozen=True, eq=True)
class TaskBase:
    title: str
    url: str
    id: str

    def to_next(self) -> 'TaskNext':
        return TaskNext(title=self.title, url=self.url, id=self.id)

    def to_later(self) -> 'TaskLater':
        return TaskLater(title=self.title, url=self.url, id=self.id)

    def to_new(self) -> 'TaskNew':
        return TaskNew(title=self.title, url=self.url, id=self.id)

    def to_never(self) -> 'TaskNever':
        return TaskNever(title=self.title, url=self.url, id=self.id)


@dataclass(frozen=True, eq=True)
class TaskNew(TaskBase):
    pass


@dataclass(frozen=True, eq=True)
class TaskNext(TaskBase):
    pass


@dataclass(frozen=True, eq=True)
class TaskLater(TaskBase):
    pass

@dataclass(frozen=True, eq=True)
class TaskNever(TaskBase):
    pass


@dataclass(frozen=True, eq=True)
class ExternalProject:
    name: str
    key: str

@dataclass(frozen=True, eq=True)
class ExternalTask:
    name: str
    url: str
    id: str
    project: ExternalProject
