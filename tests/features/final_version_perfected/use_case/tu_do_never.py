import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from ytreza_dev.features.final_version_perfected.types import TaskBase, TaskNew, TaskNext, TaskNever
from ytreza_dev.features.final_version_perfected.use_case.do_never import DoNever


@pytest.mark.parametrize("before, url, after", [
    [
        [
            TaskNew(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com")
        ],
        "https://url_2.com",
        [
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNever(title="buy the water", url="https://url_2.com")
        ]
    ],
    [
        [
            TaskNew(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com"),
            TaskNew(title="buy the bread", url="https://url_3.com")
        ],
        "https://url_3.com",
        [
            TaskNext(title="buy the milk", url="https://url_1.com"),
            TaskNew(title="buy the water", url="https://url_2.com"),
            TaskNever(title="buy the bread", url="https://url_3.com")
        ]
    ],
])
def test_do_later(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskRepositoryForTest()
    task_repository.feed(tasks=before)

    DoNever(task_repository).execute(url=url)

    assert task_repository.all_tasks() == after
