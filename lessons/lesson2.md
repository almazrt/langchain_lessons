# Урок 2: Работа с памятью и сложными цепочками в LangChain

## Введение

В предыдущем уроке мы познакомились с основами LangChain и создали простое приложение для генерации ответов на вопросы. В этом уроке мы рассмотрим более продвинутые концепции: работу с памятью для сохранения контекста между вызовами и создание сложных цепочек обработки данных.

## Память в LangChain

Память (Memory) - это важный компонент LangChain, который позволяет сохранять информацию между вызовами цепочек. Это особенно полезно при создании чат-ботов и других приложений, где требуется сохранение истории разговора.

### Типы памяти

1. **ConversationBufferMemory** - хранит всю историю разговора в виде строки
2. **ConversationSummaryMemory** - хранит краткое содержание разговора
3. **ConversationBufferWindowMemory** - хранит только последние N сообщений
4. **ConversationSummaryBufferMemory** - комбинирует буфер и сводку

## Установка зависимостей

Если вы еще не установили необходимые зависимости, выполните:

```bash
pip install langchain==1.1.0 langchain-openai python-dotenv langchain-community langchain-classic
```

## Работа с памятью в LangChain

### Подключение необходимых библиотек

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_classic.memory import ConversationBufferMemory
```

### Инициализация модели и памяти

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

# Инициализируем память
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
```

### Создание шаблона промпта с учетом истории

```python
# Создаем шаблон для чат-бота с учетом истории разговора
prompt_template = PromptTemplate.from_template(
    "Ты полезный ассистент. Отвечай на вопросы пользователя, учитывая историю разговора.\n\n"
    "История разговора:\n{chat_history}\n\n"
    "Вопрос пользователя: {question}\n"
    "Ответ:"
)
```

### Создание цепочки с памятью

```python
# Создаем последовательность из промпта, памяти и модели
chain = prompt_template | llm
```

## Полный код примера с памятью

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory

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
        
        # Инициализируем память
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Создаем шаблон для чат-бота с учетом истории разговора
        prompt_template = PromptTemplate.from_template(
            "Ты полезный ассистент. Отвечай на вопросы пользователя, учитывая историю разговора.\n\n"
            "История разговора:\n{chat_history}\n\n"
            "Вопрос пользователя: {question}\n"
            "Ответ:"
        )
        
        # Создаем цепочку
        chain = prompt_template | llm
        
        # Пример диалога
        questions = [
            "Какие основные принципы объектно-ориентированного программирования?",
            "Можешь объяснить понятнее про инкапсуляцию?",
            "А как насчет полиморфизма?"
        ]
        
        chat_history = ""
        
        for question in questions:
            print(f"\nПользователь: {question}")
            
            # Получаем ответ
            response = chain.invoke({
                "chat_history": chat_history,
                "question": question
            })
            
            answer = response.content
            print(f"Ассистент: {answer}")
            
            # Обновляем историю разговора
            chat_history += f"Пользователь: {question}\nАссистент: {answer}\n"
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()
```

## Работа со сложными цепочками

В LangChain v1.1.0 цепочки создаются с использованием оператора `|` (pipe), который объединяет различные компоненты.

### Пример сложной цепочки

```python
# Создание сложной цепочки с несколькими шагами
chain = (
    prompt_template 
    | llm 
    | lambda x: x.content.upper()  # Преобразование ответа в верхний регистр
)
```

### Параллельная обработка

```python
from langchain_core.runnables import RunnableParallel

# Создание параллельной обработки
parallel_chain = RunnableParallel({
    "original": lambda x: x,
    "uppercase": lambda x: x.upper(),
    "length": lambda x: len(x)
})

result = parallel_chain.invoke("Привет, мир!")
# Результат: {"original": "Привет, мир!", "uppercase": "ПРИВЕТ, МИР!", "length": 12}
```

## Практическое задание

1. Создайте чат-бота с использованием ConversationBufferWindowMemory, который хранит только последние 3 сообщения
2. Реализуйте цепочку, которая сначала переводит текст на английский язык, а затем генерирует краткое содержание
3. Создайте приложение, которое использует параллельную обработку для анализа тональности текста и подсчета слов

## Советы и лучшие практики

1. Выбирайте подходящий тип памяти в зависимости от задачи и объема истории разговора
2. Очищайте память при необходимости, чтобы избежать превышения лимитов контекста модели
3. Используйте асинхронные методы (`ainvoke`, `astream`) для повышения производительности
4. Логируйте взаимодействия для отладки и мониторинга
5. Обрабатывайте ошибки сети и API корректно

## Заключение

В этом уроке мы рассмотрели работу с памятью в LangChain и создание сложных цепочек обработки данных. Мы научились сохранять контекст между вызовами и строить многоступенчатые процессы обработки информации. В следующем уроке мы изучим работу с внешними данными и индексами.