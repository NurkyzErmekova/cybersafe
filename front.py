import streamlit as st
import requests

# Streamlit Веб-интерфейси
st.set_page_config(page_title="CyberSafe Teen", page_icon="🛡️")
st.title("🛡️ CyberSafe Teen — Ваша цифровая безопасность")
st.caption("Анализатор фишинга, угроз в сети и правил цифровой гигиены (на базе JSON и ИИ)")

with st.expander("📌 Описание проблемы и цели проекта"):
    st.markdown("""
- **Проблема:** Подростки часто сталкиваются с мошенничеством, фишингом и кибербуллингом в сети.
- **Цель проекта:** Создать умного помощника на базе ИИ и структурированной JSON-базы знаний для мгновенного анализа угроз.
    """)

user_text = st.text_area(
    "Вставьте подозрительное сообщение, ссылку или опишите ситуацию:",
    placeholder="Пример: Мне пришла ссылка 'Вы выиграли iPhone! Перейдите по ссылке vk-win.ru'..."
)

if st.button("Проверить на угрозы"):
    if user_text.strip():
        with st.spinner("Анализируем ситуацию..."):
            try:
                # FastAPI серверге запрос жиберебиз
                response = requests.post(
                    "http://127.0.0.1:8000/check",
                    json={"text": user_text}
                )

                if response.status_code == 200:
                    data = response.json()
                    st.subheader("💡 Результат анализа:")
                    st.write(data["analysis"])
                else:
                    st.error(f"Ошибка сервера: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Не удалось подключиться к бэкенду! Убедитесь, что FastAPI сервер запущен.")
    else:
        st.warning("Пожалуйста, введите текст для проверки.")