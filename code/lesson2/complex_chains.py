import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Проверяем наличие API ключа
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в переменных окружения или файле .env")
            return
        
        # Инициализируем модель через OpenRouter
        llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Пример параллельной обработки
        print("=== Пример параллельной обработки ===")
        parallel_chain = RunnableParallel({
            "original": lambda x: x,
            "uppercase": lambda x: x.upper(),
            "length": lambda x: len(x)
        })
        
        result = parallel_chain.invoke("Привет, мир!")
        print(f"Результат параллельной обработки: {result}")
        
        # Пример сложной цепочки с несколькими шагами
        print("\n=== Пример сложной цепочки ===")
        
        # Шаблон для перевода текста
        translation_prompt = PromptTemplate.from_template(
            "Переведи следующий текст на английский язык:\n\n{text}"
        )
        
        # Шаблон для создания краткого содержания
        summary_prompt = PromptTemplate.from_template(
            "Создай краткое содержание следующего текста:\n\n{text}"
        )
        
        # Цепочка для перевода
        translation_chain = translation_prompt | llm
        
        # Цепочка для суммаризации
        summary_chain = summary_prompt | llm
        
        # Сложная цепочка: перевод -> суммаризация
        complex_chain = translation_chain | (lambda x: {"text": x.content}) | summary_chain
        
        # Текст для обработки
        russian_text = "LangChain - это фреймворк для разработки приложений, работающих с языковыми моделями. Он предоставляет стандартные абстракции и инструменты для создания приложений, которые используют большие языковые модели."
        
        print(f"Исходный текст: {russian_text}")
        
        # Выполняем перевод
        translation_result = translation_chain.invoke({"text": russian_text})
        print(f"Перевод: {translation_result.content}")
        
        # Выполняем суммаризацию
        summary_result = summary_chain.invoke({"text": translation_result.content})
        print(f"Краткое содержание: {summary_result.content}")
        
        # Выполняем сложную цепочку
        complex_result = complex_chain.invoke({"text": russian_text})
        print(f"Результат сложной цепочки: {complex_result.content}")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()