from pyqure import pyqure, PyqureMemory, Key

from tests.features.final_version_perfected.test_choose_task_use_case import ChooseTaskUseCase
from tests.features.final_version_perfected.test_start_fvp_use_case import TodolistReaderForTest, task_repository
from ytreza_dev.features.final_version_perfected.close_task_use_case import CloseTaskUseCase
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase, ExternalTask, TaskRepository, \
    TODOLIST_READER_KEY, TASK_REPOSITORY_KEY
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import NextActionFvpQuery, TaskReader, TASK_READER_KEY
from ytreza_dev.shared.final_version_perfected.types import ChooseTaskBetween, TaskNew, TaskBase, Task, TaskNext, \
    TaskLater, DoTheTask


# class TodolistReaderForTest(start.TodolistReader):
#     def all_tasks(self) -> list[start.Task]:
#         return [
#             start.Task(name="Email ", url="https://url_1.com"),
#             start.Task(name="In-Tray", url="https://url_2.com"),
#             start.Task(name="Voicemail", url="https://url_3.com"),
#             start.Task(name="Project X Report", url="https://url_4.com"),
#             start.Task(name="Tidy Desk", url="https://url_5.com"),
#             start.Task(name="Call Dissatisfied Customer", url="https://url_6.com"),
#             start.Task(name="Make Dental Appointment", url="https://url_7.com"),
#             start.Task(name="File Invoices", url="https://url_8.com"),
#             start.Task(name="Discuss Project Y with Bob", url="https://url_9.com"),
#             start.Task(name="Back Up  ", url="https://url_10.com"),
#         ]


class TaskInMemory:
    def __init__(self) -> None:
        self._tasks: list[TaskBase] = []

    def all_tasks(self) -> list[TaskBase]:
        return self._tasks

    def save(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks

TASK_IN_MEMORY_KEY = Key("task_in_memory", TaskInMemory)



class TaskRepositoryForDemo(TaskRepository):
    def all_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()

    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def save(self, tasks: list[TaskBase]) -> None:
        self._memory.save(tasks)


class TaskReaderForDemo(TaskReader):
    def __init__(self, memory: TaskInMemory):
        self._memory = memory

    def all_active_tasks(self) -> list[TaskBase]:
        return self._memory.all_tasks()


class FvpController:
    def __init__(self, dependencies: PyqureMemory):
        (_, self._inject) = pyqure(dependencies)

    def start_fvp_session(self):
        todolist_reader = self._inject(TODOLIST_READER_KEY)
        task_repository = self._inject(TASK_REPOSITORY_KEY)

        StartFvpUseCase(todolist_reader=todolist_reader, task_repository=task_repository).execute()

    def next_action(self):
        TASK_READER_KEY = Key("task_reader", TaskReader)
        return NextActionFvpQuery(task_reader=self._inject(TASK_READER_KEY)).next_action()

    def choose_task(self, url: str):
        ChooseTaskUseCase(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)

    def close_task(self, url):
        CloseTaskUseCase(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)


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
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(TASK_REPOSITORY_KEY, TaskRepositoryForDemo(memory=task_in_memory))
    provide(TASK_IN_MEMORY_KEY, task_in_memory)
    provide(TASK_READER_KEY, TaskReaderForDemo(inject(TASK_IN_MEMORY_KEY)))

    controller = FvpController(dependencies=dependencies)
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
    assert controller.next_action() == DoTheTask(Task(title="Tidy Desk", url="https://url_5.com"))

    controller.close_task(url="https://url_5.com")
    assert controller.next_action() == ChooseTaskBetween((
        Task(title="Voicemail", url="https://url_3.com"),
        Task(title="Call Dissatisfied Customer", url="https://url_6.com")))


    # ChooseTaskUseCase(task_repository=task_repository).execute(url="https://url_1.com")
