from pyqure import PyqureMemory, pyqure # type: ignore

from tests.features.final_version_perfected.test_choose_task_use_case import ChooseTaskUseCase
from ytreza_dev.features.final_version_perfected.close_task_use_case import CloseTaskUseCase
from ytreza_dev.features.final_version_perfected.injection_keys import TODOLIST_READER_KEY, TASK_REPOSITORY_KEY, \
    TASK_READER_KEY
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.shared.final_version_perfected.types import NextAction


class FvpController:
    def __init__(self, dependencies: PyqureMemory) -> None:
        (_, self._inject) = pyqure(dependencies)

    def start_fvp_session(self) -> None:
        todolist_reader = self._inject(TODOLIST_READER_KEY)
        task_repository = self._inject(TASK_REPOSITORY_KEY)

        StartFvpUseCase(todolist_reader=todolist_reader, task_repository=task_repository).execute()

    def next_action(self) -> NextAction :
        return NextActionFvpQuery(task_reader=self._inject(TASK_READER_KEY)).next_action()

    def choose_task(self, url: str) -> None:
        ChooseTaskUseCase(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)

    def close_task(self, url: str) -> None:
        CloseTaskUseCase(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)
