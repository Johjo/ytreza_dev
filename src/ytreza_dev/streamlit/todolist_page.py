from pathlib import Path

import streamlit as st
from pyqure import pyqure, PyqureMemory  # type: ignore

from ytreza_dev.features.final_version_perfected.adapter.external_todolist_from_todoist import \
    ExternalTodolistFromTodoist
from ytreza_dev.features.final_version_perfected.adapter.task_reader_from_json import TaskReaderFromJson
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.final_version_perfected.adapter.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_READER_KEY, TODOLIST_READER_KEY, \
    TASK_REPOSITORY_KEY, EXTERNAL_TODOLIST_KEY
from ytreza_dev.features.final_version_perfected.types import ChooseTaskBetween, DoTheTask, NothingToDo
from ytreza_dev.shared.env_reader import EnvReaderFromEnv


def provide_dependencies() -> PyqureMemory:
    dependencies: PyqureMemory = {}
    (provide, inject) = pyqure(dependencies)
    env_reader = EnvReaderFromEnv(env_path=".env")
    todolist_reader = TodolistReaderFromTodoist(env_reader=env_reader)

    provide(TODOLIST_READER_KEY, todolist_reader)
    provide(TASK_REPOSITORY_KEY, TaskRepositoryFromJson(file_path=Path(env_reader.read(key="FVP_JSON_PATH"))))
    provide(TASK_READER_KEY, TaskReaderFromJson(json_path=Path(env_reader.read(key="FVP_JSON_PATH"))))
    provide(EXTERNAL_TODOLIST_KEY, ExternalTodolistFromTodoist(env_reader=env_reader))

    return dependencies

def todolist_page() -> None:
    st.title("Todolist")
    
    controller = FvpController(dependencies=provide_dependencies())
    
    if st.button("Start FVP Session"):
        controller.start_fvp_session()
    
    next_action = controller.next_action()
    if isinstance(next_action, NothingToDo):
        st.write("Nothing to do!")
    elif isinstance(next_action, ChooseTaskBetween):
        tasks = next_action.tasks
        
        # Top task
        st.title(f"{tasks[0].title}")
        col1, _, _, _, col5 = st.columns(5)
        with col1:
            st.link_button(f"Open URL", url=tasks[0].url)

        with col5:
            if st.button(f"Close", key=f"close_top_{tasks[0].url}"):
                controller.close_task(tasks[0].url)
                st.rerun()

        st.markdown("---")
        
        # Bottom task
        st.title(f"{tasks[1].title}")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.link_button(f"Open URL", url=tasks[1].url)

        with col2:
            if st.button(f"Choose", key=f"choose_bottom_{tasks[1].url}"):
                controller.choose_task(tasks[1].url)
                st.rerun()

        with col3:
            if st.button(f"Later", key=f"later_bottom_{tasks[1].url}"):
                controller.do_later(tasks[1].url)
                st.rerun()
        with col4:
            if st.button(f"Never", key=f"never_bottom_{tasks[1].url}"):
                controller.do_never(tasks[1].url)
                st.rerun()
        with col5:
            if st.button(f"Close", key=f"close_bottom_{tasks[1].url}"):
                controller.close_task(tasks[1].url)
                st.rerun()

    elif isinstance(next_action, DoTheTask):
        st.title(f"Do this task: {next_action.task.title}")
        col1, col2 = st.columns(2)
        with col1:
            st.link_button(f"Open URL", url=next_action.task.url)
        with col2:
            if st.button(f"Close", key=f"close_bottom_{next_action.task.url}"):
                controller.close_task(next_action.task.url)
                st.rerun()


