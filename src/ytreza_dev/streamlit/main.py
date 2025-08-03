import streamlit as st

from ytreza_dev.features.start_fvp_use_case.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.start_fvp_use_case.task_repository_from_json import TaskRepositoryFromJson
from ytreza_dev.features.start_fvp_use_case.use_case import StartFvpUseCase
from ytreza_dev.features.todolist_query_fvp.next_action_fvp_query import NextActionFvpQuery
from pathlib import Path

from ytreza_dev.features.todolist_query_fvp.task_reader_from_json import TaskReaderFromJson
from ytreza_dev.shared.env_reader import EnvReaderFromEnv
from ytreza_dev.shared.final_version_perfected.types import NothingToDo, DoTheTask, ChooseTaskBetween
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def main() -> None:
    st.set_page_config(page_title="Ytreza Dev Project")

    st.title("Ytreza Dev Project")

    st.header("Démarrer une session FVP")

    if st.button("Synchroniser les tâches depuis Todoist"):
        try:
            # Initialiser les composants nécessaires
            json_path = Path("data_test/tasks.json")

            start_fvp_use_case = StartFvpUseCase(TodolistReaderFromTodoist(EnvReaderFromEnv()),
                                                 TaskRepositoryFromJson(file_path=json_path))
            start_fvp_use_case.execute()

            next_action_query = NextActionFvpQuery(TaskReaderFromJson(json_path))
            next_action = next_action_query.next_action()

            # Afficher le résultat
            st.header("Prochaines actions")

            if isinstance(next_action, NothingToDo):
                st.success("Rien à faire pour le moment.")
            elif isinstance(next_action, DoTheTask):
                st.write("Prochaine tâche à faire :")
                st.write(f"Titre : {next_action.task.title}")
                st.link_button("Aller à la tâche", url=next_action.task.url)
            elif isinstance(next_action, ChooseTaskBetween):
                st.write("Choisissez entre ces deux tâches :")
                for task in next_action.tasks:
                    st.write(f"Titre : {task.title}")
                    st.link_button(f"Aller à {task.title}", url=task.url)

        except ValueError as e:
            st.error(f"Une erreur s'est produite : {e}")
        # except Exception as e:
        #     st.error(f"Échec de la synchronisation des tâches. Erreur : {e}")


if __name__ == "__main__":
    main()
