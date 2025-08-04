import streamlit as st

from ytreza_dev.streamlit.todolist_page import todolist_page


def hello_world_page() -> None:
    st.title("Hello World")


def main() -> None:
    st.set_page_config(page_title="Ytreza Dev Project", layout="wide")
    
    page = st.sidebar.radio("Navigate", ["Hello World", "Todolist"])
    
    if page == "Hello World":
        hello_world_page()
    elif page == "Todolist":
        todolist_page()

if __name__ == "__main__":
    main()
