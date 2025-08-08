import pytest

from ytreza_dev.features.final_version_perfected.query.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.features.final_version_perfected.port.task_reader import TaskReader
from ytreza_dev.features.final_version_perfected.types import Task, NothingToDo, DoTheTask, ChooseTaskBetween, TaskBase, \
    TaskNew, TaskNext, TaskLater, TaskNever


class TaskReaderForTest(TaskReader):
    def __init__(self) -> None:
        self._tasks: list[TaskBase] = []

    def feed(self, tasks: list[TaskBase]) -> None:
        self._tasks = tasks

    def all_active_tasks(self) -> list[TaskBase]:
        return self._tasks


@pytest.fixture
def task_reader() -> TaskReaderForTest:
    return TaskReaderForTest()


@pytest.fixture
def sut(task_reader: TaskReaderForTest) -> NextActionFvpQuery:
    return NextActionFvpQuery(task_reader)


class TestDoNothing:
    def test_do_nothing_when_no_task(self, sut: NextActionFvpQuery) -> None:
        next_action = sut.next_action()
        assert next_action == NothingToDo()


class TestDoTheTask:
    def test_do_next_task_when_only_one_task(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        task_reader.feed([TaskNew(title="buy the milk", url="https://url_1.com", id="1")])
        next_action = sut.next_action()
        assert next_action == DoTheTask(task=Task(title="buy the milk", url="https://url_1.com"))

    def test_06(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNext(title="buy the eggs", url="https://url_3.com", id="3"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))

    def test_07(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNext(title="buy the water", url="https://url_2.com", id="2"),
            TaskNext(title="buy the eggs", url="https://url_3.com", id="3"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))

    def test_04(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNext(title="buy the water", url="https://url_2.com", id="2"),
            TaskLater(title="buy the eggs", url="https://url_3.com", id="3"), ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the water", url="https://url_2.com"))

    def test_08(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskLater(title="buy the water", url="https://url_2.com", id="2"),
            TaskNext(title="buy the eggs", url="https://url_3.com", id="3"),
            TaskLater(title="buy the bread", url="https://url_4.com", id="4"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))


class TestChooseTaskBetween:
    def test_01(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNew(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))

    def test_02(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskLater(title="buy the bread", url="https://url_3.com", id="3"),
            TaskNew(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))
    def test_03(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskLater(title="buy the bread", url="https://url_3.com", id="3"),
            TaskLater(title="buy the eggs", url="https://url_4.com", id="4"),
            TaskNew(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))

    def test_dont_propose_never_task(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNever(title="buy the bread", url="https://url_3.com", id="3"),
            TaskNew(title="buy the water", url="https://url_2.com", id="2")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))


    def test_should_ignore_first_never_task(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNever(title="buy the milk", url="https://url_1.com", id="1"),
            TaskNew(title="buy the water", url="https://url_2.com", id="2"),
            TaskNever(title="buy the bread", url="https://url_3.com", id="3"),
            TaskNew(title="buy the butter", url="https://url_4.com", id="4")
        ])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the water", url="https://url_2.com"),
                Task(title="buy the butter", url="https://url_4.com")
            ))

