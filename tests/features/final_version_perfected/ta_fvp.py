from pyqure import pyqure, PyqureMemory  # type: ignore

from tests.features.final_version_perfected.adapters import TaskInMemory, TaskRepositoryForDemo, TASK_IN_MEMORY_KEY, \
    TaskReaderForDemo
from tests.features.final_version_perfected.fixtures import an_external_task, a_task_new, an_external_project, a_project
from tests.features.final_version_perfected.use_case.tu_start_fvp import TodolistReaderForTest
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_READER_KEY, TODOLIST_READER_KEY, \
    TASK_REPOSITORY_KEY, EXTERNAL_TODOLIST_KEY
from ytreza_dev.features.final_version_perfected.port.external_todolist import ExternalTodolistPort
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ChooseTaskBetween, Task, DoTheTask, \
    NothingToDo


def test_fvp_later() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    project = a_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    todolist_reader.feed([
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
)
    task_in_memory = TaskInMemory()
    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader))
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
        Task(title="Email ", url="https://url_1.com"),
        Task(title="In-Tray", url="https://url_2.com")))

    controller.do_later(url="https://url_2.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Voicemail", url="https://url_3.com")))

    controller.do_next(url="https://url_3.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Project X Report", url="https://url_4.com")))

    controller.do_later(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Tidy Desk", url="https://url_5.com")))

    controller.do_next(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.do_later(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.do_later(url="https://url_9.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Back Up  ", url="https://url_10.com")))

    controller.do_later(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Tidy Desk", url="https://url_5.com"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.do_later(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.do_later(url="https://url_9.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Back Up  ", url="https://url_10.com")))

    controller.do_next(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Back Up  ", url="https://url_10.com"))

    controller.close_task(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Voicemail", url="https://url_3.com"))

    controller.close_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Project X Report", url="https://url_4.com")))

    controller.do_later(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.do_next(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.do_next(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Discuss Project Y with Bob", url="https://url_9.com"))

    controller.close_task(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Make Dental Appointment", url="https://url_7.com"))

    controller.close_task(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Email ', url='https://url_1.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Email ', url='https://url_1.com'))

    controller.close_task(url="https://url_1.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com'),
               Task(title='Project X Report', url='https://url_4.com')))

    controller.do_next(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com'),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com')))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.do_later(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Project X Report', url='https://url_4.com'))

    controller.close_task(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com'),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com')))

    controller.do_next(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Call Dissatisfied Customer', url='https://url_6.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.do_next(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='File Invoices', url='https://url_8.com'))

    controller.close_task(url="https://url_8.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Call Dissatisfied Customer', url='https://url_6.com'))

    controller.close_task(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='In-Tray', url='https://url_2.com'))

    controller.close_task(url="https://url_2.com")
    assert controller.next_action() == NothingToDo()


def test_fvp_never() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    project = a_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    todolist_reader.feed([
        an_external_task(name="Email ", url="https://url_1.com", id="1", project=external_project),
        an_external_task(name="In-Tray", url="https://url_2.com", id="2", project=external_project),
        an_external_task(name="Voicemail", url="https://url_3.com", id="3", project=external_project),
        an_external_task(name="Project X Report", url="https://url_4.com", id="4", project=external_project),
        an_external_task(name="Tidy Desk", url="https://url_5.com", id="5", project=external_project),
        an_external_task(name="Call Dissatisfied Customer", url="https://url_6.com", id="6", project=external_project),
    ]
    )
    task_in_memory = TaskInMemory()
    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader))
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
        Task(title="Email ", url="https://url_1.com"),
        Task(title="In-Tray", url="https://url_2.com")))

    controller.do_never(url="https://url_2.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Voicemail", url="https://url_3.com")))

    controller.do_later(url="https://url_3.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Project X Report", url="https://url_4.com")))

    controller.do_next(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Project X Report", url="https://url_4.com"),
        Task(title="Tidy Desk", url="https://url_5.com")))

    controller.do_never(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Project X Report", url="https://url_4.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_later(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Project X Report", url="https://url_4.com"))

    controller.close_task(url="https://url_4.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_later(url="https://url_6.com")

    assert controller.next_action() == DoTheTask(
        Task(title="Email ", url="https://url_1.com"))

    controller.close_task(url="https://url_1.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.do_next(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Call Dissatisfied Customer", url="https://url_6.com"))

    controller.close_task(url="https://url_6.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Voicemail", url="https://url_3.com"))

    controller.close_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title='In-Tray', url='https://url_2.com'),
        Task(title='Tidy Desk', url='https://url_5.com')))

    controller.do_later(url="https://url_5.com")
    assert controller.next_action() == DoTheTask(
        Task(title='In-Tray', url='https://url_2.com'))

    controller.close_task(url="https://url_2.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Tidy Desk", url="https://url_5.com"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == NothingToDo()


class ExternalTodolistForDemo(ExternalTodolistPort):
    def close_task(self, url: str, task_id: str) -> None:
        pass


def provide_dependencies(task_in_memory: TaskInMemory, todolist_reader: TodolistReaderPort) -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(TASK_REPOSITORY_KEY, TaskRepositoryForDemo(memory=task_in_memory))
    provide(TASK_IN_MEMORY_KEY, task_in_memory)
    provide(TASK_READER_KEY, TaskReaderForDemo(inject(TASK_IN_MEMORY_KEY)))
    provide(EXTERNAL_TODOLIST_KEY, ExternalTodolistForDemo())

    return dependencies
