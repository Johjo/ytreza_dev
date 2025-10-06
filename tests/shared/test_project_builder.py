import pytest

from features.final_version_perfected.fixtures import ProjectBuilder
from ytreza_dev.features.final_version_perfected.types import Project


@pytest.mark.parametrize("key, expected", [
    ("1", Project(key="1", name="Project 1")),
    ("2", Project(key="2", name="Project 2")),
])
def test_builder_to_project(key: str, expected: Project) -> None:
    builder = ProjectBuilder(key=key)
    assert builder.to_project() == expected
