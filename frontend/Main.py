import random

import streamlit as st
from SessionService import MainPageState
import SessionService


def search_ui():
    col1, col2 = st.columns([0.75, 0.25])

    # Первая колонка (пустая) для смещения второй колонки вправо
    with col1:
        st.title('Сomment Hub')

    # Вторая колонка для кнопки
    with col2:
        if st.button('Create new thread'):
            SessionService.main_page_state = MainPageState.NEWTHREAD
            st.rerun()

    search_query = st.text_input("Enter URLs or keywords to search", key="search")

    search_button = st.button("Find")

    results = [
        {"title": "Test1", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test2", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test3", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test4", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
    ]
    # Отображение результатов
    if results:
        for index, feedback in enumerate(results):
            st.markdown(f" ### {feedback['title']}")
            st.markdown(f" ##### {feedback['URL']}")

            st.write(f"{feedback['Platform']}")

            col1, col2 = st.columns([0.75, 0.25])
            with col1:
                st.write(f"{feedback['date']}")
            with col2:
                if st.button('Show thread', key=f"thread_{index}"):  # ID THREAD
                    SessionService.main_page_state = MainPageState.THREADDETAIL
                    st.rerun()
            st.markdown("---")
    else:
        st.write("Результаты не найдены.")

    if search_button:
        pass
        # Отправка запроса на сервер и получение результатов
        # results = search_feedback(search_query)



def new_thread():
    def create_new_thread(url, platform, content_title, comment):
        # Здесь можно добавить код для сохранения нового треда в базу данных или куда там тебе надо
        st.success("Новый тред успешно создан!")
        st.write("URL:", url)
        st.write("Платформа:", platform)
        st.write("Название контента:", content_title)
        st.write("Комментарий:", comment)

    if st.button('Back'):
        SessionService.main_page_state = MainPageState.SEARCH
        st.rerun()

    st.title("Создание нового треда")

    url = st.text_input("URL", "")
    platform = st.selectbox("Платформа", ["YouTube", "Twitch", "Instagram", "Twitter"])
    content_title = st.text_input("Название контента", "")
    comment = st.text_area("Комментарий", "")

    if st.button("Создать"):
        if url and platform and content_title and comment:
            create_new_thread(url, platform, content_title, comment)
            SessionService.main_page_state = MainPageState.THREADDETAIL
            st.rerun()
        else:
            st.warning("Пожалуйста, заполните все поля!")


def thread_detail_ui():
    def show_thread_detail(url, platform, content_title, author, date, comments):
        if st.button('Back'):
            SessionService.main_page_state = MainPageState.SEARCH
            st.rerun()

        st.title(content_title)

        st.write(f"**{platform}:** ", url)

        col1, col2 = st.columns([0.75, 0.25])
        with col1:
            st.write("**Автор:**", author)
        with col2:
            st.write(f"_{date}_")

        st.subheader("Комментарии:")

        sort_order = st.radio("Сортировка:", ("По возрастанию даты", "По убыванию даты"))
        if sort_order == "По возрастанию даты":
            comments.sort(key=lambda x: x["date"])
        else:
            comments.sort(key=lambda x: x["date"], reverse=True)

        if st.button('New feedback'):
            st.text_area("Feedback", "")
            st.button("Submit")

        # st.subheader("")
        st.write("---")

        for index, comment in enumerate(comments):
            st.write(f"**{comment['author']}**: {comment['text']}")

            if st.button(f'Edit feedback', key=f'edit_feedback_{index}'):
                edited_text = st.text_area("Feedback", comment["text"])
                if st.button("Submit"):
                    comments[index]["text"] = edited_text
                    st.success("Feedback edited successfully!")

            st.write(f"_{comment['date']}_")
            st.write("---")

    # Пример данных для отображения
    url = "https://moodle.innopolis.university/login/index.php#section-1"
    platform = "YouTube"
    content_title = "Как выжить на необитаемом острове"
    author = "SurvivorGuy1987"
    date = "2024-04-15"
    comments = [
        {"author": "Commenter1", "text": "Крутой контент!", "date": "2024-04-16"},
        {"author": "Commenter2", "text": "Я бы поступил иначе.", "date": "2024-04-17"},
        {"author": "Commenter3", "text": "Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале? Супер, а что за музыка в начале?" , "date": "2024-04-18"}
    ]

    # Показываем информацию о треде
    show_thread_detail(url, platform, content_title, author, date, comments)


if SessionService.main_page_state == MainPageState.SEARCH:
    search_ui()
elif SessionService.main_page_state == MainPageState.NEWTHREAD:
    new_thread()
elif SessionService.main_page_state == MainPageState.THREADDETAIL:
    thread_detail_ui()
