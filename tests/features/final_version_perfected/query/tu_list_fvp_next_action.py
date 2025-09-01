import datetime

import pytest
from expression import Nothing, Some

from tests.features.final_version_perfected.adapters import TaskInformation, TaskInformationReaderForTest
from tests.features.final_version_perfected.fixtures import a_project, a_fvp_task
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.query.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.features.final_version_perfected.types import TaskDetail, NothingToDo, DoTheTask, ChooseTaskBetween, TaskBase

project_1 = a_project(key="1", name="Project 1")
project_2 = a_project(key="2", name="Project 2")

TODAY = datetime.date(2023, 1, 1)
YESTERDAY = TODAY - datetime.timedelta(days=1)

class TaskFvpReaderForTest(TaskFvpReaderPort):
    def __init__(self) -> None:
        self._tasks: list[TaskBase] = []

    def feed(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks

    def all_active_tasks(self) -> list[TaskBase]:
        return self._tasks


@pytest.fixture
def task_fvp_reader() -> TaskFvpReaderForTest:
    return TaskFvpReaderForTest()


@pytest.fixture
def task_information_reader() -> TaskInformationReaderForTest:
    return TaskInformationReaderForTest()

@pytest.fixture
def sut(task_fvp_reader: TaskFvpReaderForTest,
        task_information_reader: TaskInformationReaderForTest) -> NextActionFvpQuery:
    return NextActionFvpQuery(task_fvp_reader=task_fvp_reader, task_information_reader=task_information_reader)


class TestDoNothing:
    def test_do_nothing_when_no_task(self, sut: NextActionFvpQuery) -> None:
        next_action = sut.next_action()
        assert next_action == NothingToDo()


class TestDoTheTask:
    def test_do_next_task_when_only_one_task(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery,
                                             task_information_reader: TaskInformationReaderForTest) -> None:
        task_information_reader.feed([TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Nothing, url="https://url_1.com")])
        task_fvp_reader.feed([a_fvp_task("1").to_new()])
        next_action = sut.next_action()
        assert next_action == DoTheTask(task=TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name=project_1.name, due_date=Nothing))

    def test_display_date(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery,
                                             task_information_reader: TaskInformationReaderForTest) -> None:
        task_information_reader.feed([TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Some(TODAY), url="https://url_1.com")])
        task_fvp_reader.feed([a_fvp_task("1").to_new()])
        next_action = sut.next_action()
        assert next_action == DoTheTask(task=TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name=project_1.name, due_date=Some(TODAY)))

    def test_06(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1, due_date=Nothing, url="https://url_3.com")])

        # GIVEN
        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="3").to_next(),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=TaskDetail(key="3", title="buy the eggs", url="https://url_3.com", project_name="Project 1", due_date=Nothing))

    def test_07(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1, due_date=Nothing, url="https://url_3.com")])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_next(),
            a_fvp_task(key="3").to_next(),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=TaskDetail(key="3", title="buy the eggs", url="https://url_3.com", project_name="Project 1", due_date=Nothing))

    def test_04(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="2", title="buy the water", project=project_1, due_date=Nothing, url="https://url_2.com")])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_next(),
            a_fvp_task(key="3").to_later(), ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 1", due_date=Nothing))

    def test_08(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1, due_date=Nothing, url="https://url_3.com")])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_later(),
            a_fvp_task(key="3").to_next(),
            a_fvp_task(key="4").to_later(),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=TaskDetail(key="3", title="buy the eggs", url="https://url_3.com", project_name="Project 1", due_date=Nothing))


class TestChooseTaskBetween:
    def test_01(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Nothing, url="https://url_1.com"),
            TaskInformation(key="2", title="buy the water", project=project_2, due_date=Nothing, url="https://url_2.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task("1").to_new(),
            a_fvp_task("2").to_new()])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 2", due_date=Nothing)
            ))

    def test_02(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Nothing, url="https://url_1.com"),
            TaskInformation(key="2", title="buy the water", project=project_1, due_date=Nothing, url="https://url_2.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="3").to_later(),
            a_fvp_task("2").to_new()])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 1", due_date=Nothing)
            ))

    def test_03(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Nothing, url="https://url_1.com"),
            TaskInformation(key="2", title="buy the water", project=project_1, due_date=Nothing, url="https://url_2.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="3").to_later(),
            a_fvp_task(key="4").to_later(),
            a_fvp_task(key="2").to_new()])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 1", due_date=Nothing)
            ))

    def test_dont_propose_never_task(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery,
                                     task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Nothing, url="https://url_1.com"),
            TaskInformation(key="2", title="buy the water", project=project_1, due_date=Nothing, url="https://url_2.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="3").to_never(),
            a_fvp_task("2").to_new()])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name="Project 1", due_date=Nothing),
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 1", due_date=Nothing)
            ))

    def test_should_ignore_first_never_task(self, task_fvp_reader: TaskFvpReaderForTest,
                                            sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="2", title="buy the water", project=project_1, due_date=Nothing, url="https://url_2.com"),
            TaskInformation(key="4", title="buy the butter", project=project_1, due_date=Nothing, url="https://url_4.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task(key="1").to_never(),
            a_fvp_task("2").to_new(),
            a_fvp_task(key="3").to_never(),
            a_fvp_task("4").to_new()
        ])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 1", due_date=Nothing),
                TaskDetail(key="4", title="buy the butter", url="https://url_4.com", project_name="Project 1", due_date=Nothing)
            ))

    def test_display_due_date(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery,
                task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1, due_date=Some(TODAY), url="https://url_1.com"),
            TaskInformation(key="2", title="buy the water", project=project_2, due_date=Some(YESTERDAY), url="https://url_2.com"),
        ])

        task_fvp_reader.feed([
            a_fvp_task("1").to_new(),
            a_fvp_task("2").to_new()])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                TaskDetail(key="1", title="buy the milk", url="https://url_1.com", project_name="Project 1", due_date=Some(TODAY)),
                TaskDetail(key="2", title="buy the water", url="https://url_2.com", project_name="Project 2", due_date=Some(YESTERDAY))
            ))


