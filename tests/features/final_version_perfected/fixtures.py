from dataclasses import dataclass

from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskNever, ExternalTask, \
    ExternalProject, Project, TaskBase


def a_project(key:str, name:str)-> Project:
    return Project(key=key, name=name)

def a_task_next(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskNext:
    return TaskBuilder(title=title, url=url, key=id, project=project).to_next()


def a_task_later(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskLater:
    return TaskLater(title=title, url=url, id=id)


def a_task_new(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskLater:
    return TaskNew(title=title, url=url, id=id)


def a_task_never(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskNever:
    return TaskNever(title=title, url=url, id=id)


def an_external_project(key: str, name: str):
    return ExternalProject(name=name, key=key)


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

        self.task_base = TaskBase(id=self.key, url=self.url, title=self.title)

    def to_new(self) -> TaskNew:
        return self.task_base.to_new()

    def to_next(self) -> TaskNext:
        return self.task_base.to_next()

    def to_later(self) -> TaskLater:
        return self.task_base.to_later()

    def to_never(self) ->  TaskNever:
        return self.task_base.to_never()