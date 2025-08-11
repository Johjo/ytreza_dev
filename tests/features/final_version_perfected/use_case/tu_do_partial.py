import pytest
from attr import dataclass

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest
from ytreza_dev.features.final_version_perfected.port.task_repository import TaskRepositoryPort
from ytreza_dev.features.final_version_perfected.types import TaskNext, Project, TaskNew, TaskLater, TaskBase, TaskNever


class DoPartially:
    def __init__(self, task_repository: TaskRepositoryPort) -> None:
        self._task_repository = task_repository

    def execute(self, url: str, test_id) -> None:
        before = self._task_repository.all_tasks()
        if before[0].url == url:
            after = self._first_task_done_partially(before)
        else:
            after = self._another_task_done_partially(before, url)

        self._task_repository.save(after)

    def _another_task_done_partially(self, before: list[TaskBase], url: str):
        after = []
        index = 0
        after.append(before[index].to_next())
        index += 1
        while len(before) > index and before[index].url != url:
            after.append(before[index])
            index += 1
        after.append(before[index].to_later())
        index += 1

        while len(before) > index:
            if isinstance(before[index], TaskLater):
                after.append(before[index].to_new())
            else:
                after.append(before[index])
            index += 1
        return after


    def _first_task_done_partially(self, before: list[TaskBase]) -> list[TaskBase]:
        after = []
        index = 0
        after.append(before[index].to_next())
        index += 1
        while len(before) > index and not isinstance(before[index], TaskNew):
            after.append(before[index])
            index += 1
        if len(before) > index:
            after.append(before[index].to_next())
            index += 1
        while len(before) > index:
            after.append(before[index])
            index += 1
        return after

@dataclass
class TaskBuilder:
    key: str
    url: str

    def as_new(self) -> TaskNew:
        return TaskNew(id=self.key, url=self.url, title=f"do {self.key}",
                       project=Project(key=self.key, name="Project"))

    def as_next(self) -> TaskNext:
        return TaskNext(id=self.key, url=self.url, title=f"do {self.key}",
                        project=Project(key=self.key, name="Project"))

    def as_later(self) -> TaskLater:
        return TaskLater(id=self.key, url=self.url, title=f"do {self.key}",
                         project=Project(key=self.key, name="Project"))

    def as_never(self) ->  TaskNever:
        return TaskNever(id=self.key, url=self.url, title=f"do {self.key}",
                         project=Project(key=self.key, name="Project"))
        pass


def a_task(key: str) -> TaskBuilder:
    return TaskBuilder(key=key, url=f"https://url_{key}.com")


TASKS = [a_task(key=str(i)) for i in range(5)]


@pytest.fixture
def sut(task_repository: TaskRepositoryForTest) -> DoPartially:
    return DoPartially(task_repository)


class TestSingleTaskIsAlwaysNext:
    def test_with_new(self, sut: DoPartially, task_repository: TaskRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].as_new(),
        ])

        sut.execute(url=TASKS[0].url, test_id="1")

        assert task_repository.all_tasks() == [
            TASKS[0].as_next(),
        ]

    def test_with_next(self, sut: DoPartially, task_repository: TaskRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].as_next(),
        ])

        sut.execute(url=TASKS[0].url, test_id="2")

        assert task_repository.all_tasks() == [
            TASKS[0].as_next(),
        ]


class TestWhenPartialIsFirstTask:

    @pytest.mark.parametrize("test_id, initial, expected", [
        [
            "A",
            [
                TASKS[0].as_next(),
                TASKS[1].as_new(),
            ],
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
            ]
        ],
        [
            "B",
            [
                TASKS[0].as_next(),
                TASKS[1].as_new(),
                TASKS[2].as_new(),
                TASKS[3].as_new(),
            ],
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_new(),
                TASKS[3].as_new(),
            ]
        ],
        [
            "C",
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_new(),
                TASKS[3].as_new(),
            ],
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_next(),
                TASKS[3].as_new(),
            ]
        ],
        [
            "E",
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_later(),
                TASKS[3].as_new(),
            ],
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_later(),
                TASKS[3].as_next(),
            ]
        ],
    ])
    def test_following_new_task_become_next(self, test_id, initial, expected, sut: DoPartially,
                                            task_repository: TaskRepositoryForTest):
        task_repository.feed(tasks=initial)
        sut.execute(url=TASKS[0].url, test_id=test_id)
        assert task_repository.all_tasks() == expected

    def test_always_become_next(self, sut: DoPartially, task_repository: TaskRepositoryForTest):
        task_repository.feed(tasks=[
            TASKS[0].as_new(),
            TASKS[1].as_new(),
        ])

        sut.execute(url=TASKS[0].url, test_id="D")

        assert task_repository.all_tasks() == [
            TASKS[0].as_next(),
            TASKS[1].as_next(),
        ]


class TestWhenPartialIsAnotherTask:

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.01",
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
            ],
            TASKS[1].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
            ],

        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_next(),
            ],
            TASKS[2].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_later(),
            ],
        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.03",
            [
                TASKS[0].as_new(),
                TASKS[1].as_new(),
            ],
            TASKS[1].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
            ],
        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.04",
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_next(),
                TASKS[3].as_next(),
            ],
            TASKS[3].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_next(),
                TASKS[3].as_later(),
            ],
        ],

    ])
    def test_partially_become_later(self, sut: DoPartially, task_repository: TaskRepositoryForTest, test_id: str,
                                    initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url, test_id=test_id)

        assert task_repository.all_tasks() == expected

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.01",
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_new(),
            ],

        ],
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_later(),
                TASKS[3].as_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_new(),
                TASKS[3].as_new(),
            ],

        ],

    ])
    def test_task_later_following_partially_become_new(self, sut: DoPartially, task_repository: TaskRepositoryForTest, test_id: str,
                                    initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url, test_id=test_id)

        assert task_repository.all_tasks() == expected

    @pytest.mark.parametrize("test_id, initial, url, expected", [
        [
            "TestWhenPartialIsAnotherTask.test_partially_become_later.02",
            [
                TASKS[0].as_next(),
                TASKS[1].as_next(),
                TASKS[2].as_never(),
                TASKS[3].as_later(),
            ],
            TASKS[1].url,
            [
                TASKS[0].as_next(),
                TASKS[1].as_later(),
                TASKS[2].as_never(),
                TASKS[3].as_new(),
            ],

        ],
    ])
    def test_task_never_following_partially_become_never(self, sut: DoPartially, task_repository: TaskRepositoryForTest, test_id: str,
                                    initial: list[TaskBase], url: str, expected: list[TaskBase]):
        task_repository.feed(tasks=initial)

        sut.execute(url=url, test_id=test_id)

        assert task_repository.all_tasks() == expected


