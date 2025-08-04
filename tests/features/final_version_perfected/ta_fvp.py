from pyqure import pyqure, PyqureMemory

from tests.features.final_version_perfected.adapters import TaskInMemory, TASK_IN_MEMORY_KEY, TaskRepositoryForDemo, \
    TaskReaderForDemo
from tests.features.final_version_perfected.test_start_fvp_use_case import TodolistReaderForTest
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.start_fvp_use_case.use_case import ExternalTask
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_READER_KEY, TODOLIST_READER_KEY, \
    TASK_REPOSITORY_KEY
from ytreza_dev.shared.final_version_perfected.types import ChooseTaskBetween, TaskNew, Task, DoTheTask, \
    NothingToDo


def test_fvp():
    todolist_reader = TodolistReaderForTest()
    todolist_reader.feed([
        ExternalTask(name="Email ", url="https://url_1.com"),
        ExternalTask(name="In-Tray", url="https://url_2.com"),
        ExternalTask(name="Voicemail", url="https://url_3.com"),
        ExternalTask(name="Project X Report", url="https://url_4.com"),
        ExternalTask(name="Tidy Desk", url="https://url_5.com"),
        ExternalTask(name="Call Dissatisfied Customer", url="https://url_6.com"),
        ExternalTask(name="Make Dental Appointment", url="https://url_7.com"),
        ExternalTask(name="File Invoices", url="https://url_8.com"),
        ExternalTask(name="Discuss Project Y with Bob", url="https://url_9.com"),
        ExternalTask(name="Back Up  ", url="https://url_10.com"),
    ]
)
    task_in_memory = TaskInMemory()
    controller = FvpController(dependencies=provide_dependencies(task_in_memory, todolist_reader))
    controller.start_fvp_session()

    assert task_in_memory.all_tasks() == [
        TaskNew(title="Email ", url="https://url_1.com"),
        TaskNew(title="In-Tray", url="https://url_2.com"),
        TaskNew(title="Voicemail", url="https://url_3.com"),
        TaskNew(title="Project X Report", url="https://url_4.com"),
        TaskNew(title="Tidy Desk", url="https://url_5.com"),
        TaskNew(title="Call Dissatisfied Customer", url="https://url_6.com"),
        TaskNew(title="Make Dental Appointment", url="https://url_7.com"),
        TaskNew(title="File Invoices", url="https://url_8.com"),
        TaskNew(title="Discuss Project Y with Bob", url="https://url_9.com"),
        TaskNew(title="Back Up  ", url="https://url_10.com"),
    ]

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="In-Tray", url="https://url_2.com")))

    controller.choose_task(url="https://url_1.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Voicemail", url="https://url_3.com")))

    controller.choose_task(url="https://url_3.com")

    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Project X Report", url="https://url_4.com")))

    controller.choose_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Tidy Desk", url="https://url_5.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Tidy Desk", url="https://url_5.com"),
        Task(title="Back Up  ", url="https://url_10.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Tidy Desk", url="https://url_5.com"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.choose_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Back Up  ", url="https://url_10.com")))

    controller.choose_task(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Back Up  ", url="https://url_10.com"))

    controller.close_task(url="https://url_10.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Voicemail", url="https://url_3.com"))

    controller.close_task(url="https://url_3.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Project X Report", url="https://url_4.com")))

    controller.choose_task(url="https://url_1.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))

    controller.choose_task(url="https://url_1.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Email ", url="https://url_1.com"),
        Task(title="Make Dental Appointment", url="https://url_7.com")))

    controller.choose_task(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com"),
        Task(title="File Invoices", url="https://url_8.com")))

    controller.choose_task(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Make Dental Appointment", url="https://url_7.com"),
        Task(title="Discuss Project Y with Bob", url="https://url_9.com")))

    controller.choose_task(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Discuss Project Y with Bob", url="https://url_9.com"))

    controller.close_task(url="https://url_9.com")
    assert controller.next_action() == DoTheTask(
        Task(title="Make Dental Appointment", url="https://url_7.com"))

    controller.close_task(url="https://url_7.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Email ', url='https://url_1.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.choose_task(url="https://url_1.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Email ', url='https://url_1.com'))

    controller.close_task(url="https://url_1.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com'),
               Task(title='Project X Report', url='https://url_4.com')))

    controller.choose_task(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com'),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com')))

    controller.choose_task(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Project X Report', url='https://url_4.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.choose_task(url="https://url_4.com")
    assert controller.next_action() == DoTheTask(
        task=Task(title='Project X Report', url='https://url_4.com'))

    controller.close_task(url="https://url_4.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='In-Tray', url='https://url_2.com'),
               Task(title='Call Dissatisfied Customer', url='https://url_6.com')))

    controller.choose_task(url="https://url_6.com")
    assert controller.next_action() == ChooseTaskBetween(
        tasks=(Task(title='Call Dissatisfied Customer', url='https://url_6.com'),
               Task(title='File Invoices', url='https://url_8.com')))

    controller.choose_task(url="https://url_8.com")
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


def provide_dependencies(task_in_memory, todolist_reader) -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(TASK_REPOSITORY_KEY, TaskRepositoryForDemo(memory=task_in_memory))
    provide(TASK_IN_MEMORY_KEY, task_in_memory)
    provide(TASK_READER_KEY, TaskReaderForDemo(inject(TASK_IN_MEMORY_KEY)))
    return dependencies
