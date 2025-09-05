import pytest

from tests.features.final_version_perfected.adapters import FvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import a_fvp_task
from ytreza_dev.features.final_version_perfected.types import TaskBase
from ytreza_dev.features.final_version_perfected.use_case.do_later import DoLater


@pytest.mark.parametrize("before, key, after", [
    [
        [
            a_fvp_task("1").to_new(),
            a_fvp_task("2").to_new()
        ],
        "2",
        [
            a_fvp_task(key="1").to_next(),
            a_fvp_task(key="2").to_later()
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
            a_fvp_task(key="3").to_later()
        ]
    ],
])
def test_do_later(before: list[TaskBase], key, after: list[TaskBase]) -> None:
    task_repository = FvpRepositoryForTest()
    task_repository.feed(tasks=before)

    DoLater(task_repository).execute(updated_key=key)

    assert task_repository.all_tasks() == after
