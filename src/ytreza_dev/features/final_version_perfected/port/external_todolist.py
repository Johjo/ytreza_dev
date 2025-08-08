from abc import ABC, abstractmethod


class ExternalTodolistPort(ABC):
    @abstractmethod
    def close_task(self, url: str, task_id: str) -> None:
        pass
