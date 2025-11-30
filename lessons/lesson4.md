# Урок 4: Работа с агентами в LangChain

## Введение

В предыдущих уроках мы познакомились с основами LangChain, работой с памятью, созданием сложных цепочек и обработкой внешних данных. В этом уроке мы изучим агентов - одну из самых мощных возможностей LangChain, которая позволяет создавать автономные системы, способные принимать решения и выполнять действия на основе контекста.

Агенты отличаются от цепочек тем, что они могут динамически выбирать, какие действия выполнять и в какой последовательности, в то время как в цепочках последовательность действий жестко закодирована.

## Что такое агенты?

Агенты - это компоненты LangChain, которые используют языковую модель как движок рассуждений для определения того, какие действия выполнять и в какой последовательности. Они состоят из:

1. **LLM** - языковая модель, которая принимает решения
2. **Набор инструментов (Tools)** - действия, которые может выполнять агент
3. **Исполнитель (Agent Executor)** - компонент, который управляет выполнением агента

## Установка дополнительных зависимостей

Для работы с агентами установим необходимые зависимости:

```bash
pip install langchain==1.1.0 langchain-openai langchain-community langchain-classic python-dotenv
```

## Инструменты (Tools)

Инструменты - это функции, которые агент может вызывать для выполнения определенных задач. Давайте создадим несколько простых инструментов.

### Создание пользовательского инструмента

```python
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
```

## Создание агента

Теперь давайте создадим агента, который будет использовать наши инструменты.

### Подключение необходимых библиотек

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
```

### Инициализация модели и инструментов

```python
# Загружаем переменные окружения из файла .env
load_dotenv()

# Проверяем наличие API ключа
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Ошибка: Не найден API ключ")
    exit(1)

# Инициализируем модель через OpenRouter
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Создаем список инструментов
tools = [calculate_expression, get_weather, search_wikipedia]
```

### Создание шаблона промпта для агента

```python
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
```

### Создание и запуск агента

```python
# Создаем агента
agent = create_react_agent(llm, tools, prompt)

# Создаем исполнителя агента
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
```

## Полный код примера агента

```python
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
```

## Типы агентов

LangChain предоставляет несколько типов агентов для разных задач:

### 1. ReAct Agent
Наиболее распространенный тип агента, который использует шаблон Reasoning + Action.

```python
from langchain_classic.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)
```

### 2. Structured Chat Agent
Агент, который использует структурированный формат для взаимодействия с инструментами.

```python
from langchain_classic.agents import create_structured_chat_agent

structured_agent = create_structured_chat_agent(llm, tools, prompt)
```

### 3. OpenAI Functions Agent
Агент, который использует функции OpenAI для вызова инструментов.

```python
from langchain_classic.agents import create_openai_functions_agent

functions_agent = create_openai_functions_agent(llm, tools, prompt)
```

## Практическое задание

1. Создайте агента, который может выполнять следующие задачи:
   - Решать математические задачи
   - Искать информацию в интернете (реализуйте инструмент для поиска)
   - Работать с файлами (создайте инструмент для чтения/записи файлов)
   
2. Реализуйте агента, который может отвечать на комплексные вопросы, требующие нескольких шагов для решения.

3. Создайте чат-интерфейс для взаимодействия с вашим агентом.

## Советы и лучшие практики

1. **Безопасность инструментов**: Всегда проверяйте входные данные для инструментов и ограничивайте их возможности для предотвращения злонамеренного использования.

2. **Обработка ошибок**: Реализуйте надежную обработку ошибок как для самого агента, так и для отдельных инструментов.

3. **Логирование**: Включайте подробное логирование для отладки и мониторинга работы агента.

4. **Ограничение количества шагов**: Устанавливайте максимальное количество шагов для предотвращения бесконечных циклов.

5. **Кэширование**: Используйте кэширование для часто запрашиваемой информации, чтобы уменьшить количество вызовов API.

6. **Тестирование**: Тщательно тестируйте агента с различными сценариями использования.

## Расширение функциональности

### Добавление памяти к агенту

```python
from langchain_classic.memory import ConversationBufferMemory

# Создаем память
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Добавляем память к исполнителю агента
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=True,
    memory=memory
)
```

### Создание агента с пользовательским выводом

```python
from langchain_classic.agents.output_parsers import ReActSingleInputOutputParser

# Создаем пользовательский парсер вывода
custom_parser = ReActSingleInputOutputParser()

# Используем его при создании агента
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    output_parser=custom_parser
)
```

## Заключение

В этом уроке мы рассмотрели работу с агентами в LangChain - мощной возможностью для создания автономных систем, способных принимать решения и выполнять действия. Мы научились создавать пользовательские инструменты, настраивать агентов различных типов и управлять их выполнением.

Агенты представляют собой следующий уровень развития приложений на базе языковых моделей, позволяя создавать действительно интеллектуальные системы, которые могут адаптироваться к различным задачам и контекстам. В следующем уроке мы рассмотрим продвинутые техники работы с LangChain и создание комплексных приложений.