from pyqure import PyqureMemory, pyqure # type: ignore

from ytreza_dev.features.final_version_perfected.use_case.do_partially import DoPartially
from ytreza_dev.features.final_version_perfected.use_case.do_never import DoNever
from ytreza_dev.features.final_version_perfected.use_case.do_next import DoNext
from ytreza_dev.features.final_version_perfected.injection_keys import TODOLIST_READER_KEY, FVP_REPOSITORY_KEY, \
    TASK_FVP_READER_KEY, EXTERNAL_TODOLIST_KEY, TASK_INFORMATION_REPOSITORY_KEY
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
        fvp_repository = self._inject(FVP_REPOSITORY_KEY)
        task_information_repository = self._inject(TASK_INFORMATION_REPOSITORY_KEY)

        StartFvpUseCase(todolist_reader=todolist_reader, fvp_repository=fvp_repository,task_information_repository=task_information_repository ).execute()

    def next_action(self) -> NextAction :
        return NextActionFvpQuery(task_fvp_reader=self._inject(TASK_FVP_READER_KEY), task_information_repository=self._inject(TASK_INFORMATION_REPOSITORY_KEY)).next_action()

    def close_task(self, key: str) -> None:
        CloseTaskUseCase(task_repository=self._inject(FVP_REPOSITORY_KEY), external_todolist=self._inject(EXTERNAL_TODOLIST_KEY)).execute(key)

    def do_later(self, key: str) -> None:
        DoLater(task_repository=self._inject(FVP_REPOSITORY_KEY)).execute(key)

    def do_next(self, key: str) -> None:
        DoNext(task_repository=self._inject(FVP_REPOSITORY_KEY)).execute(key)

    def do_never(self, key: str) -> None:
        DoNever(task_repository=self._inject(FVP_REPOSITORY_KEY)).execute(key)

    def do_partial(self, key: str) -> None:
        DoPartially(task_repository=self._inject(FVP_REPOSITORY_KEY)).execute(key)

