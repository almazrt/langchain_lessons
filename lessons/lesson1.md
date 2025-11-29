# Урок 1: Введение в LangChain

## Что такое LangChain?

LangChain - это фреймворк для разработки приложений, работающих с языковыми моделями. Он предоставляет стандартные абстракции и инструменты для создания приложений, которые используют большие языковые модели (LLM).

## Основные компоненты LangChain

1. **Prompts** - шаблоны для формирования запросов к языковой модели
2. **Models** - интерфейсы для взаимодействия с различными языковыми моделями
3. **Chains** - последовательности вызовов промптов и моделей
4. **Memory** - механизм хранения контекста между вызовами
5. **Indexes** - структуры данных для работы с внешними источниками информации
6. **Agents** - компоненты, которые принимают решения о том, какие действия выполнять

## Установка LangChain

Для начала работы установим LangChain:

```bash
pip install langchain==1.1.0
```

Также установим дополнительные зависимости:

```bash
pip install langchain-openai python-dotenv
```

## Настройка API ключей

Для работы с языковыми моделями через OpenRouter необходимо получить API ключ и установить его как переменную окружения.

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
OPENROUTER_API_KEY=ваш_api_ключ_здесь
```

## Первое приложение на LangChain

Давайте создадим простое приложение, которое будет генерировать ответы на вопросы с помощью языковой модели.

### Подключение необходимых библиотек

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
```

### Инициализация модели

```python
# Загружаем переменные окружения из файла .env
load_dotenv()

# Проверяем наличие API ключа
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("Ошибка: Не найден API ключ")
    exit(1)

# Инициализируем модель через OpenRouter (через OpenAI-совместимый API)
llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",  # Модель OpenRouter
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"  # Базовый URL OpenRouter
)
```

### Создание шаблона промпта

```python
# Создаем шаблон для вопросно-ответной системы
prompt_template = PromptTemplate.from_template(
    "Ответь на следующий вопрос максимально подробно:\nВопрос: {question}\nОтвет:"
)
```

### Создание цепочки (новый подход в LangChain v1.1.0)

```python
# Создаем последовательность из промпта и модели (новый подход в LangChain v1.1.0)
chain = prompt_template | llm
```

### Использование цепочки

```python
# Задаем вопрос
question = "Что такое искусственный интеллект?"

# Получаем ответ
response = chain.invoke({"question": question})
print(response.content)
```

## Полный код примера

```python
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
```

## Практическое задание

1. Создайте новый Python файл
2. Реализуйте аналогичное приложение, но измените тему вопросов на "Основы программирования"
3. Измените шаблон промпта так, чтобы ответ был не более 100 слов
4. Добавьте обработку ошибок при вызове модели

## Советы и лучшие практики

1. Всегда храните API ключи в переменных окружения, а не в коде
2. Используйте четкие и конкретные промпты для получения лучших результатов
3. Тестируйте свои цепочки с различными входными данными
4. Не забывайте об обработке ошибок при работе с внешними API
5. Используйте виртуальное окружение для изоляции зависимостей

## Заключение

В этом уроке мы познакомились с основами LangChain и создали простое приложение для генерации ответов на вопросы. В следующем уроке мы рассмотрим более сложные цепочки и работу с памятью.