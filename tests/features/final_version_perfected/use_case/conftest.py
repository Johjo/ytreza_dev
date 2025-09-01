import pytest

from tests.features.final_version_perfected.adapters import TaskFvpRepositoryForTest


@pytest.fixture
def task_repository() -> TaskFvpRepositoryForTest:
    return TaskFvpRepositoryForTest()
