from dataclasses import dataclass

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
    return ExternalTask(name=name, url=url, id=id, project=project)


@dataclass
class TaskBuilder:
    key: str
    url: str
    title: str | None = None
    project: Project | None = None

    def __post_init__(self):
        if self.title is None:
            self.title = f"do {self.key}"

        if self.project is None:
            self.project = Project(key=self.key, name="Project")

        self.task_base = TaskBase(id=self.key)

    def to_new(self) -> TaskNew:
        return self.task_base.to_new()

    def to_next(self) -> TaskNext:
        return self.task_base.to_next()

    def to_later(self) -> TaskLater:
        return self.task_base.to_later()

    def to_never(self) ->  TaskNever:
        return self.task_base.to_never()