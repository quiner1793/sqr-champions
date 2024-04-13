import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080/feedback/search"


def search_feedback(query):
    """ Отправляет поисковый запрос на сервер и получает результаты. """
    response = requests.get(f"{API_URL}", params={"query": query, "url" : False})
    if response.status_code == 200:
        return response.json()  # Предполагается, что сервер возвращает JSON
    return []


st.title('Поисковая система фидбека')

# Поисковая строка
search_query = st.text_input("Введите поисковый запрос", key="search")

# Кнопка для поиска
search_button = st.button("Поиск")

if search_button and search_query:
    # Отправка запроса на сервер и получение результатов
    results = search_feedback(search_query)

    # results = [
    #     {"title":"Hello", "date": "12.01.123"},
    #     {"title": "Hello1", "date": "12.01.123"},
    #     {"title": "Hello2", "date": "12.01.123"},
    #     {"title": "Hello3", "date": "12.01.123"}
    # ]

    # Отображение результатов
    print(results)
    if results:
        for feedback in results:
            st.subheader(feedback['title'])
            st.write(f"Дата: {feedback['date']}")
            st.markdown("---")  # Линия для разделения карточек
    else:
        st.write("Результаты не найдены.")
