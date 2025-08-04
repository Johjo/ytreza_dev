import os
from abc import ABC, abstractmethod

from dotenv import load_dotenv


class EnvReaderPort(ABC):
    @abstractmethod
    def read(self, key: str) -> str:
        pass

class EnvReaderFromEnv(EnvReaderPort):
    def __init__(self, env_path: str) -> None:
        load_dotenv(env_path)

    def read(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"env key {key} is not defined")
        return value
