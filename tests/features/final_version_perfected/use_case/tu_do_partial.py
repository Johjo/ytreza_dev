import pytest

from tests.features.final_version_perfected.adapters import TaskFvpRepositoryForTest
from tests.features.final_version_perfected.fixtures import TaskBuilder
from ytreza_dev.features.final_version_perfected.types import TaskBase
from ytreza_dev.features.final_version_perfected.use_case.do_partially import DoPartially


def a_task(key: str) -> TaskBuilder:
    return TaskBuilder(key=key, url=f"https://url_{key}.com")


TASKS = [a_task(key=str(i)) for i in range(5)]


@pytest.fixture
def sut(task_repository: TaskFvpRepositoryForTest) -> DoPartially:
    return DoPartially(task_repository)


class TestSingleTaskIsAlwaysNext:
    def test_with_new(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].to_new(),
        ])

        sut.execute(url=TASKS[0].url)

        assert task_repository.all_tasks() == [
            TASKS[0].to_next(),
        ]

    def test_with_next(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].to_next(),
        ])

        sut.execute(url=TASKS[0].url)

        assert task_repository.all_tasks() == [
            TASKS[0].to_next(),
        ]


class TestWhenPartialIsFirstTask:

    @pytest.mark.parametrize("test_id, initial, expected", [
        [
            "A",
            [
                TASKS[0].to_next(),
                TASKS[1].to_new(),
            ],
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
            ]
        ],
        [
            "B",
            [
                TASKS[0].to_next(),
                TASKS[1].to_new(),
                TASKS[2].to_new(),
                TASKS[3].to_new(),
            ],
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_new(),
                TASKS[3].to_new(),
            ]
        ],
        [
            "C",
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_new(),
                TASKS[3].to_new(),
            ],
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_next(),
                TASKS[3].to_new(),
            ]
        ],
        [
            "E",
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_later(),
                TASKS[3].to_new(),
            ],
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_later(),
                TASKS[3].to_next(),
            ]
        ],
    ])
    def test_following_new_task_become_next(self, test_id, initial, expected, sut: DoPartially,
                                            task_repository: TaskFvpRepositoryForTest):
        task_repository.feed(tasks=initial)
        sut.execute(url=TASKS[0].url)
        assert task_repository.all_tasks() == expected

    def test_always_become_next(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].to_new(),
            TASKS[1].to_new(),
        ])

        sut.execute(url=TASKS[0].url)

        assert task_repository.all_tasks() == [
            TASKS[0].to_next(),
            TASKS[1].to_next(),
        ]


class TestWhenPartialIsAnotherTask:

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.01",
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
            ],
            TASKS[1].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
            ],

        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_next(),
            ],
            TASKS[2].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_later(),
            ],
        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.03",
            [
                TASKS[0].to_new(),
                TASKS[1].to_new(),
            ],
            TASKS[1].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
            ],
        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.04",
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_next(),
                TASKS[3].to_next(),
            ],
            TASKS[3].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_next(),
                TASKS[3].to_later(),
            ],
        ],

    ])
    def test_partially_become_later(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest, test_id: str,
                                    initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url)

        assert task_repository.all_tasks() == expected

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.01",
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_new(),
            ],

        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_later(),
                TASKS[3].to_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_new(),
                TASKS[3].to_new(),
            ],

        ],

    ])
    def test_task_later_following_partially_become_new(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest, test_id: str,
                                                       initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url)

        assert task_repository.all_tasks() == expected

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].to_next(),
                TASKS[1].to_next(),
                TASKS[2].to_never(),
                TASKS[3].to_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].to_next(),
                TASKS[1].to_later(),
                TASKS[2].to_never(),
                TASKS[3].to_new(),
            ],

        ],
    ])
    def test_task_never_following_partially_become_never(self, sut: DoPartially, task_repository: TaskFvpRepositoryForTest, test_id: str,
                                                         initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url)

        assert task_repository.all_tasks() == expected


