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


@dataclass()
class TaskBase:
    title: str
    url: str


@dataclass
class TaskNew(TaskBase):
    pass


@dataclass
class TaskNext(TaskBase):
    pass


@dataclass
class TaskLater(TaskBase):
    pass


