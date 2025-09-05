import pytest

from tests.features.final_version_perfected.adapters import FvpRepositoryForTest


@pytest.fixture
def task_repository() -> FvpRepositoryForTest:
    return FvpRepositoryForTest()
