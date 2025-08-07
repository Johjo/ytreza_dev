from abc import ABC, abstractmethod


class ExternalTodolistPort(ABC):
    @abstractmethod
    def close_task(self, url: str) -> None:
        pass
