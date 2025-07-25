import streamlit as st

from ytreza_dev.features.todolist_query.todolist_reader_from_todoist import TodolistReaderFromTodoist
from ytreza_dev.features.todolist_query.todolist_query import TodolistQuery


def main() -> None:
    st.set_page_config(page_title="Ytreza Dev Project")

    st.title("Ytreza Dev Project")
    st.write("Hello World")

    st.header("Todoist Tasks")

    if st.button("Load tasks from Todoist"):
        try:
            # It's good practice to instantiate these here so that
            # they are re-created on each button click, which avoids
            # potential state issues in a Streamlit app.
            adapter = TodolistReaderFromTodoist()
            todolist_query = TodolistQuery(adapter)
            tasks = todolist_query.all_tasks()

            if tasks:
                st.write("Here are your tasks:")
                # Display tasks in a simple table
                st.table([{"Task Name": task.name} for task in tasks])
            else:
                st.success("No tasks found in your Todoist account.")

        except ValueError as e:
            # This will catch the error if the API token is not set
            st.error(f"An error occurred: {e}")
        except Exception as e:
            # Catch other potential errors (e.g., network issues)
            st.error(f"Failed to fetch tasks from Todoist. Error: {e}")


if __name__ == "__main__":
    main()
