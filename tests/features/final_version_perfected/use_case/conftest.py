import pytest

from tests.features.final_version_perfected.adapters import TaskRepositoryForTest


@pytest.fixture
def task_repository() -> TaskRepositoryForTest:
    return TaskRepositoryForTest()
