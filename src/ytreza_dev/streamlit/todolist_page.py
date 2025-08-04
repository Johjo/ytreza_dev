from pathlib import Path

import streamlit as st
from pyqure import pyqure, PyqureMemory  # type: ignore

from ytreza_dev.features.final_version_perfected.adapter.task_reader_from_json import TaskReaderFromJson
from ytreza_dev.features.final_version_perfected.adapter.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.final_version_perfected.adapter.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.final_version_perfected.controller import FvpController
from ytreza_dev.features.final_version_perfected.injection_keys import TASK_READER_KEY, TODOLIST_READER_KEY, TASK_REPOSITORY_KEY
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
        st.write("Choose between tasks:")
        for task in next_action.tasks:
            st.title(f"{task.title}")
            if st.button(f"Choose", key=f"choose {task.url}"):
                controller.choose_task(task.url)
                st.rerun()
            if st.button(f"Close", key=f"close {task.url}"):
                controller.close_task(task.url)
                st.rerun()
            if st.button(f"Open", key=f"open {task.url}"):
                controller.close_task(task.url)
                st.rerun()
    elif isinstance(next_action, DoTheTask):
        st.write(f"Do this task: {next_action.task.title}")
        if st.button(f"Close task: {next_action.task.title}"):
            controller.close_task(next_action.task.url)
            st.rerun()
