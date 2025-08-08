from pyqure import PyqureMemory, pyqure # type: ignore

from ytreza_dev.features.final_version_perfected.use_case.do_never import DoNever
from ytreza_dev.features.final_version_perfected.use_case.do_next import DoNext
from ytreza_dev.features.final_version_perfected.injection_keys import TODOLIST_READER_KEY, TASK_REPOSITORY_KEY, \
    TASK_READER_KEY, EXTERNAL_TODOLIST_KEY
from ytreza_dev.features.final_version_perfected.use_case.close_task_use_case import CloseTaskUseCase
from ytreza_dev.features.final_version_perfected.use_case.do_later import DoLater
from ytreza_dev.features.final_version_perfected.use_case.start_fvp_use_case import StartFvpUseCase
from ytreza_dev.features.final_version_perfected.query.next_action_fvp_query import NextActionFvpQuery
from ytreza_dev.features.final_version_perfected.types import NextAction


class FvpController:
    def __init__(self, dependencies: PyqureMemory) -> None:
        (_, self._inject) = pyqure(dependencies)

    def start_fvp_session(self) -> None:
        todolist_reader = self._inject(TODOLIST_READER_KEY)
        task_repository = self._inject(TASK_REPOSITORY_KEY)

        StartFvpUseCase(todolist_reader=todolist_reader, task_repository=task_repository).execute()

    def next_action(self) -> NextAction :
        return NextActionFvpQuery(task_reader=self._inject(TASK_READER_KEY)).next_action()

    def close_task(self, url: str) -> None:
        CloseTaskUseCase(task_repository=self._inject(TASK_REPOSITORY_KEY), external_todolist=self._inject(EXTERNAL_TODOLIST_KEY)).execute(url)

    def do_later(self, url: str) -> None:
        DoLater(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)

    def do_next(self, url: str) -> None:
        DoNext(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)

    def do_never(self, url: str) -> None:
        DoNever(task_repository=self._inject(TASK_REPOSITORY_KEY)).execute(url)
