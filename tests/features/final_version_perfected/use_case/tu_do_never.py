import pytest

from tests.features.final_version_perfected.adapters import TaskFvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_fvp_task
from ytreza_dev.features.final_version_perfected.types import TaskBase
from ytreza_dev.features.final_version_perfected.use_case.do_never import DoNever


@pytest.mark.parametrize("before, url, after", [
    [
        [
            a_fvp_task("1").to_new(),
            a_fvp_task("2").to_new()
        ],
        "2",
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_never()
        ]
    ],
    [
        [
            a_fvp_task("1").to_new(),
            a_fvp_task("2").to_new(),
            a_fvp_task("3").to_new()
        ],
        "3",
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task("2").to_new(),
            a_fvp_task(key="3").to_never()
        ]
    ],
])
def test_do_later(before: list[TaskBase], url: str, after: list[TaskBase]) -> None:
    task_repository = TaskFvpRepositoryForTest()
    task_repository.feed(tasks=before)

    DoNever(task_repository).execute(updated_key=url)

    assert task_repository.all_tasks() == after
