import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

@tool
def calculate_expression(expression: str) -> float:
    """Выполняет математические вычисления. Используйте этот инструмент для решения математических задач.
    
    Args:
        expression: Математическое выражение для вычисления (например, "2 + 3 * 4")
    
    Returns:
        float: Результат вычисления
    """
    try:
        # Безопасное вычисление выражения
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            raise ValueError("Выражение содержит недопустимые символы")
        
        result = eval(expression)
        return float(result)
    except Exception as e:
        return f"Ошибка при вычислении: {str(e)}"

@tool
def get_weather(city: str) -> str:
    """Получает информацию о погоде в указанном городе.
    
    Args:
        city: Название города
        
    Returns:
        str: Информация о погоде
    """
    # В реальном приложении здесь был бы вызов API погоды
    weather_data = {
        "Москва": "Сейчас в Москве солнечно, 22°C",
        "Санкт-Петербург": "В Санкт-Петербурге облачно, 18°C",
        "Новосибирск": "В Новосибирске дождь, 15°C",
        "Екатеринбург": "В Екатеринбурге ясно, 20°C"
    }
    
    return weather_data.get(city, f"Информация о погоде для {city} недоступна")

@tool
def search_wikipedia(query: str) -> str:
    """Выполняет поиск информации в Википедии.
    
    Args:
        query: Поисковый запрос
        
    Returns:
        str: Краткая информация по запросу
    """
    # В реальном приложении здесь был бы вызов API Википедии
    wikipedia_data = {
        "искусственный интеллект": "Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием программного обеспечения и алгоритмов, наделяющих компьютеры способностью к обучению, рассуждению и принятию решений.",
        "машинное обучение": "Машинное обучение — это подраздел искусственного интеллекта, который изучает алгоритмы и статистические модели, которые компьютерные системы используют для выполнения задач без явных инструкций.",
        "нейронная сеть": "Нейронная сеть — это вычислительная система, имитирующая работу биологических нейронных сетей головного мозга."
    }
    
    for key, value in wikipedia_data.items():
        if key in query.lower():
            return value
    
    return f"Информация по запросу '{query}' не найдена в Википедии"

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
        tools = [calculate_expression, get_weather, search_wikipedia]

        # Создаем шаблон для агента ReAct
        template = """Ты полезный ассистент, который может использовать инструменты для ответа на вопросы.
Используй инструменты только когда это необходимо для ответа на вопрос.

Доступные инструменты:
{tools}

Используй следующий формат:

Вопрос: вопрос, на который нужно ответить
Thought: твой ход мыслей о том, что делать
Action: действие, которое нужно выполнить, должно быть одним из [{tool_names}]
Action Input: входные данные для действия
Observation: результат действия
... (этот цикл Thought/Action/Action Input/Observation может повторяться N раз)
Thought: теперь я знаю ответ
Final Answer: финальный ответ на оригинальный вопрос

Начнем!

Вопрос: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)

        # Создаем агента
        agent = create_react_agent(llm, tools, prompt)

        # Создаем исполнителя агента
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

        # Примеры вопросов
        questions = [
            "Сколько будет 15 умножить на 4 минус 10?",
            "Какая сейчас погода в Москве?",
            "Что такое искусственный интеллект?",
            "Рассчитай площадь круга с радиусом 5 см",
            "Какая погода в Париже и что такое машинное обучение?"
        ]

        print("=== Демонстрация работы агента ===")
        for question in questions:
            print(f"\nВопрос: {question}")
            try:
                result = agent_executor.invoke({"input": question})
                print(f"Ответ: {result['output']}")
            except Exception as e:
                print(f"Ошибка при обработке вопроса: {str(e)}")

    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()