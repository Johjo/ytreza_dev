import os
from abc import ABC, abstractmethod


class EnvReaderPort(ABC):
    @abstractmethod
    def read(self, key: str) -> str:
        pass

class EnvReaderFromEnv(EnvReaderPort):
    def read(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"env key {key} is not defined")
        return value
