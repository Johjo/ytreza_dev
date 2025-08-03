import os
from abc import ABC


class EnvReaderPort(ABC):
    def read(self, key) -> str:
        value = os.getenv(key)
        if value is None:
            raise KeyError(f"env key {key} is not defined")
        return value


class EnvReaderFromEnv(EnvReaderPort):
    pass
