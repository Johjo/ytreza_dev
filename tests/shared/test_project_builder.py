import pytest

from tests.features.final_version_perfected.fixtures import ProjectBuilder
from ytreza_dev.features.final_version_perfected.types import Project, ExternalProject


@pytest.mark.parametrize("key, expected", [
    ("1", Project(key="1", name="Project 1")),
    ("2", Project(key="2", name="Project 2")),
])
def test_builder_with_default_value(key: str, expected: Project) -> None:
    builder = ProjectBuilder(key=key)
    assert builder.to_project() == expected


def test_builder_to_project() -> None:
    builder = ProjectBuilder(key="23", name="project name")
    assert builder.to_project() == Project(key="23", name="project name")


@pytest.mark.parametrize("sut, expected", [
    [ProjectBuilder(key="123"), ExternalProject(key="123", name="Project 123")],
    [ProjectBuilder(key="23", name="project name"), ExternalProject(key="23", name="project name")],
])
def test_builder_to_external(sut: ProjectBuilder, expected: ExternalProject) -> None:
    assert sut.to_external() == expected

