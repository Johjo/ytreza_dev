from ytreza_dev.features.final_version_perfected.types import TaskNext, TaskLater, TaskNew, TaskNever, ExternalTask


def a_task_next(title: str, url:str, id: str) -> TaskNext:
    return TaskNext(title=title, url=url, id=id)


def a_task_later(title: str, url:str, id: str) -> TaskLater:
    return TaskLater(title=title, url=url, id=id)


def a_task_new(title: str, url:str, id: str) -> TaskLater:
    return TaskNew(title=title, url=url, id=id)


def a_task_never(title: str, url:str, id: str) -> TaskNever:
    return TaskNever(title=title, url=url, id=id)


def an_external_task(name: str, url: str, id: str) -> ExternalTask:
    return ExternalTask(name=name, url=url, id=id)
