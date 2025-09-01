from attr import dataclass

from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskNever, ExternalTask, \
    ExternalProject, Project


def a_project(key:str, name:str)-> Project:
    return Project(key=key, name=name)

def a_task_next(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskNext:
    return TaskNext(title=title, url=url, id=id, project=project)


def a_task_later(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskLater:
    return TaskLater(title=title, url=url, id=id, project=project)


def a_task_new(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskLater:
    return TaskNew(title=title, url=url, id=id, project=project)


def a_task_never(title: str, url:str, id: str, project:Project = a_project(key="1", name="Project 1")) -> TaskNever:
    return TaskNever(title=title, url=url, id=id, project=project)


def an_external_project(key: str, name: str):
    return ExternalProject(name=name, key=key)


def an_external_task(name: str, url: str, id: str,
                     project: ExternalProject = ExternalProject(name="Project", key="1")) -> ExternalTask:
    return ExternalTask(name=name, url=url, id=id, project=project)


@dataclass
class TaskBuilder:
    key: str
    url: str

    def as_new(self) -> TaskNew:
        return TaskNew(id=self.key, url=self.url, title=f"do {self.key}",
                       project=Project(key=self.key, name="Project"))

    def as_next(self) -> TaskNext:
        return TaskNext(id=self.key, url=self.url, title=f"do {self.key}",
                        project=Project(key=self.key, name="Project"))

    def as_later(self) -> TaskLater:
        return TaskLater(id=self.key, url=self.url, title=f"do {self.key}",
                         project=Project(key=self.key, name="Project"))

    def as_never(self) ->  TaskNever:
        return TaskNever(id=self.key, url=self.url, title=f"do {self.key}",
                         project=Project(key=self.key, name="Project"))
        pass
