import pytest

from tests.features.final_version_perfected.adapters import TaskInformation, TaskInformationReaderForTest
from tests.features.final_version_perfected.fixtures import a_task_new, a_task_next, a_task_later, a_task_never, \
    a_project
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskFvpReaderPort
from ytreza_dev.features.final_version_perfected.query.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.features.final_version_perfected.types import Task, NothingToDo, DoTheTask, ChooseTaskBetween, TaskBase

project_1 = a_project(key="1", name="Project 1")
project_2 = a_project(key="2", name="Project 2")


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
        task_information_reader.feed([TaskInformation(key="1", title="buy the milk", project=project_1)])
        task_fvp_reader.feed([a_task_new(title="buy the milk", url="https://url_1.com", id="1", project=project_1)])
        next_action = sut.next_action()
        assert next_action == DoTheTask(task=Task(title="buy the milk", url="https://url_1.com", project_name=project_1.name))

    def test_06(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1)])

        # GIVEN
        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_next(title="buy the eggs", url="https://url_3.com", id="3"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com", project_name="Project 1"))

    def test_07(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1)])

        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_next(title="buy the water", url="https://url_2.com", id="2"),
            a_task_next(title="buy the eggs", url="https://url_3.com", id="3"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com", project_name="Project 1"))

    def test_04(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="2", title="buy the water", project=project_1)])

        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_next(title="buy the water", url="https://url_2.com", id="2"),
            a_task_later(title="buy the eggs", url="https://url_3.com", id="3"), ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the water", url="https://url_2.com", project_name="Project 1"))

    def test_08(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader: TaskInformationReaderForTest) -> None:
        # GIVEN
        task_information_reader.feed([TaskInformation(key="3", title="buy the eggs", project=project_1)])

        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_later(title="buy the water", url="https://url_2.com", id="2"),
            a_task_next(title="buy the eggs", url="https://url_3.com", id="3"),
            a_task_later(title="buy the bread", url="https://url_4.com", id="4"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com", project_name="Project 1"))


class TestChooseTaskBetween:
    def test_01(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1),
            TaskInformation(key="2", title="buy the water", project=project_2),
        ])

        task_fvp_reader.feed([
            a_task_new(title="buy the milk", url="https://url_1.com", id="1", project=project_1),
            a_task_new(title="buy the water", url="https://url_2.com", id="2", project=project_2)])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com", project_name="Project 1"),
                Task(title="buy the water", url="https://url_2.com", project_name="Project 2")
            ))

    def test_02(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1),
            TaskInformation(key="2", title="buy the water", project=project_1),
        ])


        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_later(title="buy the bread", url="https://url_3.com", id="3"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com", project_name="Project 1"),
                Task(title="buy the water", url="https://url_2.com", project_name="Project 1")
            ))

    def test_03(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1),
            TaskInformation(key="2", title="buy the water", project=project_1),
        ])


        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_later(title="buy the bread", url="https://url_3.com", id="3"),
            a_task_later(title="buy the eggs", url="https://url_4.com", id="4"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com", project_name="Project 1"),
                Task(title="buy the water", url="https://url_2.com", project_name="Project 1")
            ))

    def test_dont_propose_never_task(self, task_fvp_reader: TaskFvpReaderForTest, sut: NextActionFvpQuery,
                                     task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="1", title="buy the milk", project=project_1),
            TaskInformation(key="2", title="buy the water", project=project_1),
        ])


        task_fvp_reader.feed([
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_never(title="buy the bread", url="https://url_3.com", id="3"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com", project_name="Project 1"),
                Task(title="buy the water", url="https://url_2.com", project_name="Project 1")
            ))

    def test_should_ignore_first_never_task(self, task_fvp_reader: TaskFvpReaderForTest,
                                            sut: NextActionFvpQuery, task_information_reader) -> None:
        # GIVEN
        task_information_reader.feed([
            TaskInformation(key="2", title="buy the water", project=project_1),
            TaskInformation(key="4", title="buy the butter", project=project_1),
        ])


        task_fvp_reader.feed([
            a_task_never(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2"),
            a_task_never(title="buy the bread", url="https://url_3.com", id="3"),
            a_task_new(title="buy the butter", url="https://url_4.com", id="4")
        ])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the water", url="https://url_2.com", project_name="Project 1"),
                Task(title="buy the butter", url="https://url_4.com", project_name="Project 1")
            ))

