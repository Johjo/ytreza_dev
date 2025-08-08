import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from ytreza_dev.features.final_version_perfected.types import TaskNew, TaskLater, TaskNext, TaskBase
from ytreza_dev.features.final_version_perfected.use_case.choose_task import ChooseTaskUseCase


def test_repository() -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed([TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
                          TaskNew(title="buy the water", url="https://url_2.com", id="2")])

    assert task_repository.all_tasks() == [TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
                                           TaskNew(title="buy the water", url="https://url_2.com", id="2")]


@pytest.mark.parametrize("before, url, after", [
    [[TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNew(title="buy the water", url="https://url_2.com", id="2")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2")]],

    [[TaskNew(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNew(title="buy the water", url="https://url_2.com", id="2")],
     "https://url_2.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNext(title="buy the water", url="https://url_2.com", id="2")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNext(title="buy the water", url="https://url_2.com", id="2"),
      TaskNew(title="buy the eggs", url="https://url_3.com", id="3")],
     "https://url_2.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNext(title="buy the water", url="https://url_2.com", id="2"),
      TaskLater(title="buy the eggs", url="https://url_3.com", id="3")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskNew(title="buy the eggs", url="https://url_3.com", id="3")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskLater(title="buy the eggs", url="https://url_3.com", id="3")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskNew(title="buy the eggs", url="https://url_3.com", id="3")],
     "https://url_3.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskNext(title="buy the eggs", url="https://url_3.com", id="3")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNew(title="buy the water", url="https://url_2.com", id="2"),
      TaskNew(title="buy the eggs", url="https://url_3.com", id="3")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskNew(title="buy the eggs", url="https://url_3.com", id="3")]],

    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskLater(title="buy the eggs", url="https://url_3.com", id="3"),
      TaskNew(title="buy the bread", url="https://url_4.com", id="4")],
     "https://url_1.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskLater(title="buy the water", url="https://url_2.com", id="2"),
      TaskLater(title="buy the eggs", url="https://url_3.com", id="3"),
      TaskLater(title="buy the bread", url="https://url_4.com", id="4")]],


    [[TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNext(title="buy the water", url="https://url_2.com", id="2"),
      TaskNext(title="buy the eggs", url="https://url_3.com", id="3"),
      TaskNew(title="buy the bread", url="https://url_4.com", id="4")],
     "https://url_4.com",
     [TaskNext(title="buy the milk", url="https://url_1.com", id="1"),
      TaskNext(title="buy the water", url="https://url_2.com", id="2"),
      TaskNext(title="buy the eggs", url="https://url_3.com", id="3"),
      TaskNext(title="buy the bread", url="https://url_4.com", id="4")]],
])
def test_xxx(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(before)
    sut = ChooseTaskUseCase(task_repository)

    sut.execute(url=url)

    assert task_repository.all_tasks() == after
