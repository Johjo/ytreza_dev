from expression import Nothing
from pyqure import pyqure, PyqureMemory  # type: ignore

from tests.features.final_version_perfected.fixtures import an_external_task, an_external_project, \
    a_fvp_task
from tests.features.final_version_perfected.use_case.tu_start_fvp import TodolistReaderForTest
from ytreza_dev.features.final_version_perfected.adapter.for_demo import TASK_IN_MEMORY_KEY, \
    TaskFvpReaderForDemo, TaskInMemory, FvpRepositoryForDemo, ExternalTodolistForDemo, TaskInformationRepositoryForDemo
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_FVP_READER_KEY, TODOLIST_READER_KEY, \
    FVP_REPOSITORY_KEY, EXTERNAL_TODOLIST_KEY, TASK_INFORMATION_REPOSITORY_KEY
from ytreza_dev.features.final_version_perfected.port.todolist_reader import TodolistReaderPort
from ytreza_dev.features.final_version_perfected.types import ChooseTaskBetween, TaskDetail, DoTheTask, \
    NothingToDo


def test_fvp_later() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
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


    task_in_memory = TaskInMemory()
    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader))
    controller.start_fvp_session()

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="2", title="In-Tray", url="https://url_2.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="2")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="3")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="4")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="5")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="7")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="8", title="File Invoices", url="https://url_8.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="8")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="9", title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="9")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="10", title="Back Up  ", url="https://url_10.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="10")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="5")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="7")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="8", title="File Invoices", url="https://url_8.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="8")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="9", title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="9")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="10", title="Back Up  ", url="https://url_10.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="10")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="10", title="Back Up  ", url="https://url_10.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="10")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="3")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="4")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="7")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="8", title="File Invoices", url="https://url_8.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="8")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="9", title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="9")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="9", title="Discuss Project Y with Bob", url="https://url_9.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="9")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="7", title="Make Dental Appointment", url="https://url_7.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="7")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="1", title='Email ', url='https://url_1.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="8", title='File Invoices', url='https://url_8.com', project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="8")
    assert controller.next_action() == DoTheTask(
        task=TaskDetail(key="1", title='Email ', url='https://url_1.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="1")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="2", title='In-Tray', url='https://url_2.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="4", title='Project X Report', url='https://url_4.com', project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="4")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="4", title='Project X Report', url='https://url_4.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="6", title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="4", title='Project X Report', url='https://url_4.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="8", title='File Invoices', url='https://url_8.com', project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="8")
    assert controller.next_action() == DoTheTask(
        task=TaskDetail(key="4", title='Project X Report', url='https://url_4.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="4")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="2", title='In-Tray', url='https://url_2.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="6", title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="6")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(TaskDetail(key="6", title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1", due_date=Nothing),
               TaskDetail(key="8", title='File Invoices', url='https://url_8.com', project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="8")
    assert controller.next_action() == DoTheTask(
        task=TaskDetail(key="8", title='File Invoices', url='https://url_8.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="8")
    assert controller.next_action() == DoTheTask(
        task=TaskDetail(key="6", title='Call Dissatisfied Customer', url='https://url_6.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="6")
    assert controller.next_action() == DoTheTask(
        task=TaskDetail(key="2", title='In-Tray', url='https://url_2.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="2")
    assert controller.next_action() == NothingToDo()


def test_fvp_never() -> None:
    external_project = an_external_project(key="1", name="Project 1")
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

    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        a_fvp_task("1").to_new(),
        a_fvp_task("2").to_new(),
        a_fvp_task("3").to_new(),
        a_fvp_task("4").to_new(),
        a_fvp_task("5").to_new(),
        a_fvp_task("6").to_new(),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="2", title="In-Tray", url="https://url_2.com", project_name="Project 1", due_date=Nothing)))

    controller.do_never(key="2")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="3")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="4")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing)))

    controller.do_never(key="5")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="4", title="Project X Report", url="https://url_4.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="4")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="6")

    assert controller.next_action() == DoTheTask(
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="1")

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing)))

    controller.do_next(key="6")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="6", title="Call Dissatisfied Customer", url="https://url_6.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="6")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="3", title="Voicemail", url="https://url_3.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="3")
    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="2", title='In-Tray', url='https://url_2.com', project_name="Project 1", due_date=Nothing),
        TaskDetail(key="5", title='Tidy Desk', url='https://url_5.com', project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="5")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="2", title='In-Tray', url='https://url_2.com', project_name="Project 1", due_date=Nothing))

    controller.close_task(key="2")
    assert controller.next_action() == DoTheTask(
        TaskDetail(key="5", title="Tidy Desk", url="https://url_5.com", project_name="Project 1", due_date=Nothing))

    controller.close_task(key="5")
    assert controller.next_action() == NothingToDo()



def provide_dependencies(task_in_memory: TaskInMemory, todolist_reader: TodolistReaderPort) -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(FVP_REPOSITORY_KEY, FvpRepositoryForDemo(memory=task_in_memory))
    provide(TASK_IN_MEMORY_KEY, task_in_memory)
    provide(TASK_FVP_READER_KEY, TaskFvpReaderForDemo(inject(TASK_IN_MEMORY_KEY)))
    provide(EXTERNAL_TODOLIST_KEY, ExternalTodolistForDemo())
    provide(TASK_INFORMATION_REPOSITORY_KEY, TaskInformationRepositoryForDemo())
    return dependencies


def test_do_partial() -> None:
    external_project = an_external_project(key="1", name="Project 1")
    todolist_reader = TodolistReaderForTest()
    external_tasks = [
        an_external_task(name="Email ", url="https://url_1.com", id="1", project=external_project),
        an_external_task(name="In-Tray", url="https://url_2.com", id="2", project=external_project),
        an_external_task(name="Voicemail", url="https://url_3.com", id="3", project=external_project),
    ]
    todolist_reader.feed(external_tasks
                         )
    task_in_memory = TaskInMemory()
    controller = FvpController(
        dependencies=provide_dependencies(task_in_memory, todolist_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        a_fvp_task("1").to_new(),
        a_fvp_task("2").to_new(),
        a_fvp_task("3").to_new(),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        TaskDetail(key="1", title="Email ", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
        TaskDetail(key="2", title="In-Tray", url="https://url_2.com", project_name="Project 1", due_date=Nothing)))

    controller.do_later(key="2")

    assert controller.next_action() == ChooseTaskBetween(tasks=(
        TaskDetail(key="1", title='Email ', url='https://url_1.com', project_name='Project 1', due_date=Nothing),
        TaskDetail(key="3", title='Voicemail', url='https://url_3.com', project_name='Project 1', due_date=Nothing)))

    controller.do_next(key='3')

    assert controller.next_action() == DoTheTask(task=(
        TaskDetail(key="3", title='Voicemail', url='https://url_3.com', project_name='Project 1', due_date=Nothing)))

    controller.do_partial(key='3')

    assert task_in_memory.all_tasks() == [
        a_fvp_task(key="1").to_next(),
        a_fvp_task(key="2").to_later(),
        a_fvp_task(key="3").to_later(),
    ]

