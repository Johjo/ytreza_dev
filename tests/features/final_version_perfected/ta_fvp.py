from pyqure import pyqure, PyqureMemory  # type: ignore

from tests.features.final_version_perfected.adapters import TaskInMemory, TaskRepositoryForDemo, TASK_IN_MEMORY_KEY, \
    TaskFvpReaderForDemo
from tests.features.final_version_perfected.fixtures import an_external_task, a_task_new, an_external_project, \
    a_project, a_task_later, a_task_next
from tests.features.final_version_perfected.use_case.tu_start_fvp import TodolistReaderForTest
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_FVP_READER_KEY, TODOLIST_READER_KEY, \
    TASK_REPOSITORY_KEY, EXTERNAL_TODOLIST_KEY, TASK_INFORMATION_READER_KEY
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.port.task_information_reader import TaskInformationReaderPort, \
    TaskInformation
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ChooseTaskBetween, Task, DoTheTask, \
    NothingToDo, ExternalTask


def test_fvp_later() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    project = a_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    task_information_reader = TaskInformationReaderForDemo()
    external_tasks = [
        an_external_task(name="Email ", url="https://url_1.com", id="1", project=external_project),
        an_external_task(name="In-Tray", url="https://url_2.com", id="2", project=external_project),
        an_external_task(name="Voicemail", url="https://url_3.com", id="3", project=external_project),
        an_external_task(name="Project X Report", url="https://url_4.com", id="4", project=external_project),
        an_external_task(name="Tidy Desk", url="https://url_5.com", id="5", project=external_project),
        an_external_task(name="Call Dissatisfied Customer", url="https://url_6.com", id="6", project=external_project),
        an_external_task(name="Make Dental Appointment", url="https://url_7.com", id="7", project=external_project),
        an_external_task(name="File Invoices", url="https://url_8.com", id="8", project=external_project),
        an_external_task(name="Discuss Project Y with Bob", url="https://url_9.com", id="9", project=external_project),
        an_external_task(name="Back Up  ", url="https://url_10.com", id="10", project=external_project),
    ]
    todolist_reader.feed(external_tasks)
    task_information_reader.feed(external_tasks)


    task_in_memory = TaskInMemory()
    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader,
                                                                 task_information_reader=task_information_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        a_task_new(title="Email ", url="https://url_1.com", id="1", project=project),
        a_task_new(title="In-Tray", url="https://url_2.com", id="2", project=project),
        a_task_new(title="Voicemail", url="https://url_3.com", id="3", project=project),
        a_task_new(title="Project X Report", url="https://url_4.com", id="4", project=project),
        a_task_new(title="Tidy Desk", url="https://url_5.com", id="5", project=project),
        a_task_new(title="Call Dissatisfied Customer", url="https://url_6.com", id="6", project=project),
        a_task_new(title="Make Dental Appointment", url="https://url_7.com", id="7", project=project),
        a_task_new(title="File Invoices", url="https://url_8.com", id="8", project=project),
        a_task_new(title="Discuss Project Y with Bob", url="https://url_9.com", id="9", project=project),
        a_task_new(title="Back Up  ", url="https://url_10.com", id="10", project=project),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="In-Tray", url="https://url_2.com", project_name="Project 1")))

    controller.do_later(url="https://url_2.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1")))

    controller.do_next(url="https://url_3.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1")))

    controller.do_later(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1")))

    controller.do_next(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"),
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1")))

    controller.do_later(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"),
        Task(title="File Invoices", url="https://url_8.com", project_name="Project 1")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1")))

    controller.do_later(url="https://url_9.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"),
        Task(title="Back Up  ", url="https://url_10.com", project_name="Project 1")))

    controller.do_later(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1")))

    controller.do_later(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="File Invoices", url="https://url_8.com", project_name="Project 1")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1")))

    controller.do_later(url="https://url_9.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Back Up  ", url="https://url_10.com", project_name="Project 1")))

    controller.do_next(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Back Up  ", url="https://url_10.com", project_name="Project 1"))

    controller.close_task(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"))

    controller.close_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1")))

    controller.do_later(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1")))

    controller.do_next(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1"),
        Task(title="File Invoices", url="https://url_8.com", project_name="Project 1")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1")))

    controller.do_next(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1"))

    controller.close_task(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1"))

    controller.close_task(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Email ', url='https://url_1.com', project_name="Project 1"),
               Task(title='File Invoices', url='https://url_8.com', project_name="Project 1")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Email ', url='https://url_1.com', project_name="Project 1"))

    controller.close_task(url="https://url_1.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com', project_name="Project 1"),
               Task(title='Project X Report', url='https://url_4.com', project_name="Project 1")))

    controller.do_next(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com', project_name="Project 1"),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com', project_name="Project 1"),
               Task(title='File Invoices', url='https://url_8.com', project_name="Project 1")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Project X Report', url='https://url_4.com', project_name="Project 1"))

    controller.close_task(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com', project_name="Project 1"),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1")))

    controller.do_next(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1"),
               Task(title='File Invoices', url='https://url_8.com', project_name="Project 1")))

    controller.do_next(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='File Invoices', url='https://url_8.com', project_name="Project 1"))

    controller.close_task(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1"))

    controller.close_task(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='In-Tray', url='https://url_2.com', project_name="Project 1"))

    controller.close_task(url="https://url_2.com")
    assert controller.next_action() == NothingToDo()


def test_fvp_never() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    project = a_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    external_tasks = [
        an_external_task(name="Email ", url="https://url_1.com", id="1", project=external_project),
        an_external_task(name="In-Tray", url="https://url_2.com", id="2", project=external_project),
        an_external_task(name="Voicemail", url="https://url_3.com", id="3", project=external_project),
        an_external_task(name="Project X Report", url="https://url_4.com", id="4", project=external_project),
        an_external_task(name="Tidy Desk", url="https://url_5.com", id="5", project=external_project),
        an_external_task(name="Call Dissatisfied Customer", url="https://url_6.com", id="6", project=external_project),
    ]
    todolist_reader.feed(external_tasks)
    task_in_memory = TaskInMemory()
    task_information_reader = TaskInformationReaderForDemo()
    task_information_reader.feed(external_tasks)

    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader,
                                                                 task_information_reader=task_information_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        a_task_new(title="Email ", url="https://url_1.com", id="1", project=project),
        a_task_new(title="In-Tray", url="https://url_2.com", id="2", project=project),
        a_task_new(title="Voicemail", url="https://url_3.com", id="3", project=project),
        a_task_new(title="Project X Report", url="https://url_4.com", id="4", project=project),
        a_task_new(title="Tidy Desk", url="https://url_5.com", id="5", project=project),
        a_task_new(title="Call Dissatisfied Customer", url="https://url_6.com", id="6", project=project),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="In-Tray", url="https://url_2.com", project_name="Project 1")))

    controller.do_never(url="https://url_2.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1")))

    controller.do_later(url="https://url_3.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1")))

    controller.do_next(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1"),
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1")))

    controller.do_never(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Project X Report", url="https://url_4.com", project_name="Project 1"))

    controller.close_task(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_later(url="https://url_6.com")

    assert controller.next_action() == DoTheTask(
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"))

    controller.close_task(url="https://url_1.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1")))

    controller.do_next(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1"))

    controller.close_task(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Voicemail", url="https://url_3.com", project_name="Project 1"))

    controller.close_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title='In-Tray', url='https://url_2.com', project_name="Project 1"),
        Task(title='Tidy Desk', url='https://url_5.com', project_name="Project 1")))

    controller.do_later(url="https://url_5.com")
    assert controller.next_action() == DoTheTask(
        Task(title='In-Tray', url='https://url_2.com', project_name="Project 1"))

    controller.close_task(url="https://url_2.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Tidy Desk", url="https://url_5.com", project_name="Project 1"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == NothingToDo()


class ExternalTodolistForDemo(ExternalTodolistPort):
    def close_task(self, url: str, task_id: str) -> None:
        pass


class TaskInformationReaderForDemo(TaskInformationReaderPort):
    def __init__(self):
        self._tasks: dict[str, TaskInformation] = {}

    def by_key(self, key: str) -> TaskInformation:
        return self._tasks[key]

    def feed(self, tasks: list[ExternalTask]):
        for task in tasks:
            self._tasks[task.id] = TaskInformation(key=task.id, title=task.name, project=task.project)


def provide_dependencies(task_in_memory: TaskInMemory, todolist_reader: TodolistReaderPort,
                         task_information_reader: TaskInformationReaderPort) -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(TASK_REPOSITORY_KEY, TaskRepositoryForDemo(memory=task_in_memory))
    provide(TASK_IN_MEMORY_KEY, task_in_memory)
    provide(TASK_FVP_READER_KEY, TaskFvpReaderForDemo(inject(TASK_IN_MEMORY_KEY)))
    provide(EXTERNAL_TODOLIST_KEY, ExternalTodolistForDemo())
    provide(TASK_INFORMATION_READER_KEY, task_information_reader)

    return dependencies


def test_do_partial() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    project = a_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    external_tasks = [
        an_external_task(name="Email ", url="https://url_1.com", id="1", project=external_project),
        an_external_task(name="In-Tray", url="https://url_2.com", id="2", project=external_project),
        an_external_task(name="Voicemail", url="https://url_3.com", id="3", project=external_project),
    ]
    todolist_reader.feed(external_tasks
                         )
    task_in_memory = TaskInMemory()
    task_information_reader = TaskInformationReaderForDemo()
    task_information_reader.feed(external_tasks)
    controller = FvpController(
        dependencies=provide_dependencies(task_in_memory, todolist_reader, task_information_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        a_task_new(title="Email ", url="https://url_1.com", id="1", project=project),
        a_task_new(title="In-Tray", url="https://url_2.com", id="2", project=project),
        a_task_new(title="Voicemail", url="https://url_3.com", id="3", project=project),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com", project_name="Project 1"),
        Task(title="In-Tray", url="https://url_2.com", project_name="Project 1")))

    controller.do_later(url="https://url_2.com")

    assert controller.next_action() == ChooseTaskBetween(tasks=(
        Task(title='Email ', url='https://url_1.com', project_name='Project 1'),
        Task(title='Voicemail', url='https://url_3.com', project_name='Project 1')))

    controller.do_next(url='https://url_3.com')

    assert controller.next_action() == DoTheTask(task=(
        Task(title='Voicemail', url='https://url_3.com', project_name='Project 1')))

    controller.do_partial('https://url_3.com')

    assert task_in_memory.all_tasks() == [
        a_task_next(title="Email ", url="https://url_1.com", id="1", project=project),
        a_task_later(title="In-Tray", url="https://url_2.com", id="2", project=project),
        a_task_later(title="Voicemail", url="https://url_3.com", id="3", project=project),
    ]

