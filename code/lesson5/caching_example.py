#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Кэширование в LangChain
Этот пример демонстрирует использование кэширования для оптимизации вызовов LLM.
"""

import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# Включение кэширования в памяти
from langchain_core.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
set_llm_cache(InMemoryCache())

def caching_example():
    """Пример использования кэширования."""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в .env файле")
        return
    
    # Инициализация модели
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Создание промпта
    prompt = ChatPromptTemplate.from_template("Объясни концепцию {concept}")
    
    # Создание цепочки
    chain = prompt | llm | StrOutputParser()
    
    print("=== Демонстрация кэширования ===\n")
    
    # Первый вызов - будет выполнен реальный запрос к LLM
    print("1. Первый вызов (без кэша):")
    start_time = time.time()
    result1 = chain.invoke({"concept": "искусственный интеллект"})
    end_time = time.time()
    print(f"Результат: {result1[:100]}...")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
    
    # Второй вызов с тем же запросом - результат будет из кэша
    print("2. Второй вызов (с кэшем):")
    start_time = time.time()
    result2 = chain.invoke({"concept": "искусственный интеллект"})
    end_time = time.time()
    print(f"Результат: {result2[:100]}...")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
    
    # Третий вызов с другим запросом - будет выполнен реальный запрос
    print("3. Третий вызов (другой запрос, без кэша):")
    start_time = time.time()
    result3 = chain.invoke({"concept": "машинное обучение"})
    end_time = time.time()
    print(f"Результат: {result3[:100]}...")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
    
    # Четвертый вызов с другим запросом - будет выполнен реальный запрос
    print("4. Четвертый вызов (еще один новый запрос):")
    start_time = time.time()
    result4 = chain.invoke({"concept": "нейронные сети"})
    end_time = time.time()
    print(f"Результат: {result4[:100]}...")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
    
    # Пятый вызов с тем же запросом, что и в пункте 3 - результат будет из кэша
    print("5. Пятый вызов (повтор третьего запроса, с кэшем):")
    start_time = time.time()
    result5 = chain.invoke({"concept": "машинное обучение"})
    end_time = time.time()
    print(f"Результат: {result5[:100]}...")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд\n")
    
    print("=== Завершено ===")
    print("\nОбратите внимание на разницу во времени выполнения между кэшированными и некэшированными вызовами!")

def main():
    """Основная функция."""
    try:
        caching_example()
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()