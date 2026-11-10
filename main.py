import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. FastAPI тиркемеси
app = FastAPI(title="CyberSafe Teen API")


# 2. JSON файлынан база маалыматтарын жүктөө
def init_knowledge_base():
    try:
        with open("cyber_safety_db.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        context_parts = []
        for cat in data.get("categories", []):
            context_parts.append(f"Категория: {cat['title']}")
            for rule in cat['rules']:
                context_parts.append(f"- {rule}")

        return "\n".join(context_parts)
    except FileNotFoundError:
        return "База знаний не найдена. Проверьте файл cyber_safety_db.json."


context = init_knowledge_base()

# 3. Шаблон промпта жана LLM
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """Вы — эксперт по кибербезопасности для подростков. 
Анализируйте входящую ситуацию, находите потенциальные угрозы и давайте понятные советы, опираясь на базу знаний.

База знаний:
{context}"""),
    ("human", "{user_input}")
])

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key="sk-proj-..."  # Өзүңүздүн ключ
)

output_parser = StrOutputParser()

chain = (
        {
            "context": lambda x: context,
            "user_input": RunnablePassthrough()
        }
        | prompt_template
        | llm
        | output_parser
)


class CheckRequest(BaseModel):
    text: str


# FastAPI POST эндипоинту (Postman жана Streamlit үчүн)
@app.post("/check")
def check_threat_api(request: CheckRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Текст не может быть пустым.")

    try:
        # Эгер баланс жок болсо, төмөнкү mock_response'ту колдоно берсеңиз болот:
        response = chain.invoke(request.text)
        return {"status": "success", "analysis": response}
    except Exception as e:
        # Тестирлөө үчүн заглушка (баланс жок болсо да иштеши үчүн)
        mock_response = (
            "🛡️ [Тестирлөө режими / Симуляция]\n"
            f"Анализ текста: «{request.text}»\n\n"
            "💡 Экспертный совет:\n"
            "1. В данном запросе потенциально могут содержаться признаки фишинга или мошенничества.\n"
            "2. Никогда не переходите по неизвестным ссылкам и не вводите личные данные.\n"
            "3. Рекомендуем заблокировать отправителя и обратиться к взрослым."
        )
        return {"status": "success", "analysis": mock_response}