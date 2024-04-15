import streamlit as st

# def main

col1, col2 = st.columns([0.75, 0.25])

# Первая колонка (пустая) для смещения второй колонки вправо
with col1:
    st.title('Сomment Hub')

# Вторая колонка для кнопки
with col2:
    if st.button('Create new thread'):
        st.write("Добавление нового комментария...")

search_query = st.text_input("Enter URLs or keywords to search", key="search")

search_button = st.button("Find")

if search_button and search_query:
    # Отправка запроса на сервер и получение результатов
    # results = search_feedback(search_query)

    results = [
        {"title": "Test1", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test2", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test3", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
        {"title": "Test4", "URL": "https://telegram", "Platform": "telegram", "date": "21.0.1123"},
    ]
    # Отображение результатов
    if results:
        for feedback in results:
            st.markdown(f" ### {feedback['title']}")
            st.markdown(f" ##### {feedback['URL']}")

            st.write(f"{feedback['Platform']}")

            col1, col2 = st.columns([0.75, 0.25])
            with col1:
                st.write(f"{feedback['date']}")
            with col2:
                if st.button('Show thread', key=feedback['title']): # ID THREAD
                    ""
            st.markdown("---")
    else:
        st.write("Результаты не найдены.")
