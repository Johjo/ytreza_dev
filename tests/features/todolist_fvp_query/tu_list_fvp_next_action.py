from dataclasses import dataclass

import pytest


@dataclass
class Task:
    title: str
    url: str


@dataclass
class ChooseTaskBetween:
    tasks: (Task, Task)


@dataclass
class DoTheTask:
    task: Task


@dataclass()
class TaskBase:
    title: str
    url: str


@dataclass
class TaskNew(TaskBase):
    pass


@dataclass
class TaskNext(TaskBase):
    pass

@dataclass
class TaskLater(TaskBase):
    pass


@dataclass
class NothingToDo:
    pass


class TaskReaderForTest:
    def __init__(self) -> None:
        self._tasks: list[TaskNew] = []

    def feed(self, tasks):
        self._tasks = tasks

    def all_active_tasks(self) -> list[TaskNew]:
        return self._tasks


class NextActionFvpQuery:
    def __init__(self, task_reader: TaskReaderForTest):
        self._task_reader = task_reader

    def next_action(self) -> NothingToDo:
        tasks = self._task_reader.all_active_tasks()

        if not tasks:
            return NothingToDo()

        next_task_index = self._next_task_index(tasks)
        new_task_index = self._new_task_index(next_task_index, tasks)

        if new_task_index > next_task_index:
            return ChooseTaskBetween(tasks=(
                Task(title=tasks[next_task_index].title, url=tasks[next_task_index].url),
                Task(title=tasks[new_task_index].title, url=tasks[new_task_index].url)
            ))

        return DoTheTask(task=Task(title=tasks[next_task_index].title, url=tasks[next_task_index].url))

    @staticmethod
    def _new_task_index(next_task_index, tasks):
        return next(
            (index for index in range(next_task_index + 1, len(tasks)) if isinstance(tasks[index], TaskNew)),
            next_task_index
        )

    @staticmethod
    def _next_task_index(tasks):
        return next(
                (index for index, task in reversed(list(enumerate(tasks))) if isinstance(task, TaskNext)),
                0
        )


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
        task_reader.feed([TaskNew(title="buy the milk", url="https://url_1.com")])
        next_action = sut.next_action()
        assert next_action == DoTheTask(task=Task(title="buy the milk", url="https://url_1.com"))

    def test_06(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNext(title="buy the eggs", url="https://url_3.com"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))

    def test_07(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNext(title="buy the water", url="https://url_2.com"),
            TaskNext(title="buy the eggs", url="https://url_3.com"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))

    def test_04(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNext(title="buy the water", url="https://url_2.com"),
            TaskLater(title="buy the eggs", url="https://url_3.com"), ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the water", url="https://url_2.com"))

    def test_08(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskLater(title="buy the water", url="https://url_2.com"),
            TaskNext(title="buy the eggs", url="https://url_3.com"),
            TaskLater(title="buy the bread", url="https://url_4.com"),
        ])

        # WHEN / THEN
        assert sut.next_action() == DoTheTask(task=Task(title="buy the eggs", url="https://url_3.com"))


class TestChooseTaskBetween:
    def test_01(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNew(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))

    def test_02(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskLater(title="buy the bread", url="https://url_3.com"),
            TaskNew(title="buy the water", url="https://url_2.com")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))

    def test_03(self, task_reader: TaskReaderForTest, sut: NextActionFvpQuery) -> None:
        # GIVEN
        task_reader.feed([
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskLater(title="buy the bread", url="https://url_3.com"),
            TaskLater(title="buy the eggs", url="https://url_4.com"),
            TaskNew(title="buy the water", url="https://url_2.com")])

        # WHEN / THEN
        assert sut.next_action() == ChooseTaskBetween(
            tasks=(
                Task(title="buy the milk", url="https://url_1.com"),
                Task(title="buy the water", url="https://url_2.com")
            ))
