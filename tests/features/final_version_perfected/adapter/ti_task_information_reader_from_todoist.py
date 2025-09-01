from approvaltests import verify

from ytreza_dev.features.final_version_perfected.adapter.task_information_reader_from_todoist import \
    TaskInformationReaderFromTodoist
from ytreza_dev.shared.env_reader import EnvReaderFromEnv


def test_read_information() -> None:
    env_reader = EnvReaderFromEnv(env_path=".env.test")

    sut = TaskInformationReaderFromTodoist(env_reader=env_reader)
    information = sut.by_key("9497217837")

    verify(information, encoding="utf-8")
