import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_task_new, a_task_next, a_task_later
from ytreza_dev.features.final_version_perfected.types import TaskBase
from ytreza_dev.features.final_version_perfected.use_case.do_later import DoLater


@pytest.mark.parametrize("before, url, after", [
    [
        [
            a_task_new(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2")
        ],
        "https://url_2.com",
        [
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_later(title="buy the water", url="https://url_2.com", id="2")
        ]
    ],
    [
        [
            a_task_new(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2"),
            a_task_new(title="buy the bread", url="https://url_3.com", id="3")
        ],
        "https://url_3.com",
        [
            a_task_next(title="buy the milk", url="https://url_1.com", id="1"),
            a_task_new(title="buy the water", url="https://url_2.com", id="2"),
            a_task_later(title="buy the bread", url="https://url_3.com", id="3")
        ]
    ],
])
def test_do_later(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(tasks=before)

    DoLater(task_repository).execute(url=url)

    assert task_repository.all_tasks() == after
