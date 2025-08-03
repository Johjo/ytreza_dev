import pytest

from tests.features.final_version_perfected.test_start_fvp_use_case import TodolistReaderForTest, TaskRepositoryForTest
from tests.features.final_version_perfected.tu_list_fvp_next_action import TaskReaderForTest
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.shared.final_version_perfected.types import ChooseTaskBetween, TaskNew, Task


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


@pytest.mark.skip
def test_fvp():
    todolist_reader = TodolistReaderForTest()
    todolist_reader.feed([
            Task(title="Email ", url="https://url_1.com"),
            Task(title="In-Tray", url="https://url_2.com"),
            Task(title="Voicemail", url="https://url_3.com"),
            Task(title="Project X Report", url="https://url_4.com"),
            Task(title="Tidy Desk", url="https://url_5.com"),
            Task(title="Call Dissatisfied Customer", url="https://url_6.com"),
            Task(title="Make Dental Appointment", url="https://url_7.com"),
            Task(title="File Invoices", url="https://url_8.com"),
            Task(title="Discuss Project Y with Bob", url="https://url_9.com"),
            Task(title="Back Up  ", url="https://url_10.com"),
        ]
)
    start_fvp_use_case = StartFvpUseCase(todolist_reader=todolist_reader,
                                         task_repository=TaskRepositoryForTest())
    start_fvp_use_case.execute()

    actual = NextActionFvpQuery(task_reader=TaskReaderForTest()).next_action()
    assert actual == ChooseTaskBetween([TaskNew(title="Email ", url="https://url_1.com")])