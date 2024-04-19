import time

import streamlit as st
from SessionService import MainPageState, searchResults, Thread, selectedThread
from NetworkService import create_thread, search, get_thread_details
import SessionService
import validators


import NetworkService


def search_ui():
    col1, col2 = st.columns([0.75, 0.25])

    # Первая колонка (пустая) для смещения второй колонки вправо
    with col1:
        st.title('Сomment Hub')

    # Вторая колонка для кнопки
    with col2:
        if st.button('Create new thread'):
            SessionService.main_page_state = MainPageState.NEW_THREAD
            st.rerun()

    search_query = st.text_input("Enter URLs or keywords to search", key="search")

    search_button = st.button("Find")

    # Отображение результатов
    if len(searchResults) > 0:
        for index, feedback in enumerate(searchResults):
            st.markdown(f" ### {feedback.title}")
            st.markdown(f" ##### {feedback.link}")

            st.write(f"{feedback.platform}")

            col1, col2 = st.columns([0.75, 0.25])
            with col1:
                st.write(f"{feedback.date}")
            with col2:
                if st.button('Show thread', key=f"thread_{index}"):  # ID THREAD
                    SessionService.main_page_state = MainPageState.THREAD_DETAIL

                    SessionService.selectedThread = Thread(feedback.link_id,
                                                           feedback.link,
                                                           feedback.platform,
                                                           feedback.title,
                                                           feedback.username,
                                                           feedback.date)
                    st.rerun()
            st.markdown("---")
    else:
        st.write("No results were found :(")

    if search_button:
        print(search_query)
        if validators.url(search_query):
            SessionService.searchResults = search(True, query=search_query)
        else:
            SessionService.searchResults = search(False, query=search_query)
        st.rerun()


def new_thread():
    def create_new_thread(url, platform, content_title, comment):
        response = create_thread(url, content_title, platform, comment)

        if response[0]:
            st.success("Thread created!")
            time.sleep(0.5)
            SessionService.main_page_state = MainPageState.THREAD_DETAIL

            # TODO createThread
            SessionService.selectedThread = Thread(0, url, platform, content_title, "Me", "123")
            st.rerun()
        else:
            st.error(response[1])

    if st.button('Back'):
        SessionService.main_page_state = MainPageState.SEARCH
        st.rerun()

    st.title("Создание нового треда")

    url = st.text_input("URL", "")

    # platform = st.selectbox("Платформа", ["YouTube", "Twitch", "Instagram", "Twitter"])
    # content_title = st.text_input("Название контента", "")
    comment = st.text_area("Комментарий", "")

    if st.button("Создать"):

        platform, content_title = NetworkService.get_content_details_from_url(url)

        if url and platform and content_title and comment:
            create_new_thread(url, platform, content_title, comment)
        else:
            st.warning("Пожалуйста, заполните все поля!")


def thread_title(thread: Thread) -> None:
    st.title(thread.content_title)

    st.write(f"**{thread.platform}:** ", thread.url)

    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        st.write("**Author:**", thread.author)
    with col2:
        st.write(f"_{thread.date}_")


def feedback_title(thread: Thread) -> None:
    st.subheader("Feedback:")

    sort_order = st.radio("Сортировка:", ("По возрастанию даты", "По убыванию даты"))
    if sort_order == "По возрастанию даты":
        thread.comments.sort(key=lambda x: x.date)
    else:
        thread.comments.sort(key=lambda x: x.date, reverse=True)
    comment = st.text_area("Feedback", "")

    if st.button("Submit"):
        response = NetworkService.add_feedback(thread.link_id, comment)

        if response[0]:
            st.rerun()
        else:
            st.error(response[1])

    st.write("---")


def comments(thread: Thread) -> None:
    for index, comment in enumerate(thread.comments):

        st.write(f"**{comment.username}**: {comment.comment}")

        if comment.user_id == SessionService.get_id():
            edited_text = st.text_area("Edit", comment.comment, key=f"edited_text_area_{index}")
            if st.button("Submit", key=f'submit_{index}'):
                thread.comments[index].comment = edited_text

                response = NetworkService.edit_feedback(comment.id, edited_text)

                if response[0]:
                    st.success("Feedback edited successfully!")
                    st.rerun()
                else:
                    st.error(response[1])

        st.write(f"_{comment.date}_")
        st.write("---")


def thread_detail_ui(thread: Thread) -> None:
    if st.button('Back'):
        SessionService.main_page_state = MainPageState.SEARCH
        st.rerun()

    if thread:
        thread.comments = NetworkService.get_thread_details(thread.link_id)

        thread_title(thread)

        feedback_title(thread)

        comments(thread)

    else:
        st.error("No selected Thread")


if SessionService.main_page_state == MainPageState.SEARCH:
    search_ui()
elif SessionService.main_page_state == MainPageState.NEW_THREAD:
    new_thread()
elif SessionService.main_page_state == MainPageState.THREAD_DETAIL:
    thread_detail_ui(SessionService.selectedThread)
