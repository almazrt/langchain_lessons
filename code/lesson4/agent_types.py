import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import (
    create_react_agent, 
    create_structured_chat_agent,
    create_openai_functions_agent
)
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

@tool
def simple_calculator(a: float, b: float, operation: str) -> float:
    """Простой калькулятор для базовых математических операций.
    
    Args:
        a: Первое число
        b: Второе число
        operation: Операция ('add', 'subtract', 'multiply', 'divide')
    
    Returns:
        float: Результат операции
    """
    operations = {
        'add': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': a / b if b != 0 else "Ошибка: деление на ноль"
    }
    
    return operations.get(operation, "Неизвестная операция")

@tool
def get_current_time() -> str:
    """Возвращает текущее время."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    try:
        # Загружаем переменные окружения из файла .env
        load_dotenv()

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

        # Создаем список инструментов
        tools = [simple_calculator, get_current_time]

        print("=== Демонстрация различных типов агентов ===")
        
        # 1. ReAct Agent
        print("\n1. ReAct Agent:")
        react_template = """Ты полезный ассистент. Используй инструменты для ответа на вопросы.
        
Доступные инструменты:
{tools}

Используй следующий формат:
Вопрос: вопрос, на который нужно ответить
Thought: твой ход мыслей о том, что делать
Action: действие, которое нужно выполнить, должно быть одним из [{tool_names}]
Action Input: входные данные для действия
Observation: результат действия
Thought: теперь я знаю ответ
Final Answer: финальный ответ на оригинальный вопрос

Вопрос: {input}
{agent_scratchpad}"""

        react_prompt = PromptTemplate.from_template(react_template)
        react_agent = create_react_agent(llm, tools, react_prompt)
        react_executor = AgentExecutor(agent=react_agent, tools=tools, verbose=True, handle_parsing_errors=True)
        
        try:
            result = react_executor.invoke({"input": "Сколько будет 10 умножить на 5?"})
            print(f"ReAct Agent ответ: {result['output']}")
        except Exception as e:
            print(f"Ошибка ReAct Agent: {str(e)}")

        # 2. Structured Chat Agent
        print("\n2. Structured Chat Agent:")
        structured_template = """Ты полезный ассистент. Используй инструменты для ответа на вопросы.
        
Доступные инструменты:
{tools}

Используй инструменты с правильным синтаксисом JSON:
Action: инструмент для вызова
Action Input: JSON с входными параметрами

Вопрос: {input}
{agent_scratchpad}"""

        structured_prompt = PromptTemplate.from_template(structured_template)
        
        try:
            structured_agent = create_structured_chat_agent(llm, tools, structured_prompt)
            structured_executor = AgentExecutor(agent=structured_agent, tools=tools, verbose=True, handle_parsing_errors=True)
            
            result = structured_executor.invoke({"input": "Какое сейчас время?"})
            print(f"Structured Chat Agent ответ: {result['output']}")
        except Exception as e:
            print(f"Ошибка Structured Chat Agent: {str(e)}. Возможно, этот тип агента требует дополнительной настройки.")

    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()