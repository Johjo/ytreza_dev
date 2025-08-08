from dataclasses import dataclass
from typing import Tuple


@dataclass
class Task:
    title: str
    url: str


@dataclass
class NothingToDo:
    pass


@dataclass
class DoTheTask:
    task: Task


@dataclass
class ChooseTaskBetween:
    tasks: Tuple[Task, Task]


NextAction = NothingToDo | DoTheTask | ChooseTaskBetween

@dataclass(frozen=True, eq=True)
class Project:
    key: str
    name: str


@dataclass()
class TaskBase:
    title: str
    url: str
    id: str
    project: Project

    def to_next(self) -> 'TaskNext':
        return TaskNext(title=self.title, url=self.url, id=self.id, project=self.project)

    def to_later(self) -> 'TaskLater':
        return TaskLater(title=self.title, url=self.url, id=self.id, project=self.project)

    def to_new(self) -> 'TaskNew':
        return TaskNew(title=self.title, url=self.url, id=self.id, project=self.project)

    def to_never(self) -> 'TaskNever':
        return TaskNever(title=self.title, url=self.url, id=self.id, project=self.project)


@dataclass
class TaskNew(TaskBase):
    pass


@dataclass
class TaskNext(TaskBase):
    pass


@dataclass
class TaskLater(TaskBase):
    pass

@dataclass
class TaskNever(TaskBase):
    pass


@dataclass
class ExternalProject:
    name: str
    key: str

@dataclass
class ExternalTask:
    name: str
    url: str
    id: str
    project: ExternalProject
