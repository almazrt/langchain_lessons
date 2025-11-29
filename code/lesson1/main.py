import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Проверяем наличие API ключа
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в переменных окружения или файле .env")
            return
        
        # Инициализируем модель через OpenRouter (через OpenAI-совместимый API)
        llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",  # Модель OpenRouter
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"  # Базовый URL OpenRouter
        )
        
        # Создаем шаблон для вопросно-ответной системы
        prompt_template = PromptTemplate.from_template(
            "Ответь на следующий вопрос максимально подробно:\nВопрос: {question}\nОтвет:"
        )
        
        # Создаем последовательность из промпта и модели (новый подход в LangChain v1.1.0)
        chain = prompt_template | llm
        
        # Задаем вопрос
        question = "Что такое искусственный интеллект?"
        
        print(f"Отправляем вопрос: {question}")
        
        # Получаем ответ
        response = chain.invoke({"question": question})
        print(f"Вопрос: {question}")
        print(f"Ответ: {response.content}")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()