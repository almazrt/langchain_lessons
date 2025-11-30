#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Асинхронные цепочки в LangChain
Этот пример демонстрирует использование асинхронных цепочек для повышения производительности.
"""

import asyncio
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

async def async_chain_example():
    """Пример асинхронной цепочки."""
    # Загружаем переменные окружения
    load_dotenv()
    
    # Получаем API ключ
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в .env файле")
        return
    
    # Инициализация асинхронной модели
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=api_key,
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Создание промпта
    prompt = ChatPromptTemplate.from_template("Расскажи краткий интересный факт о {topic}")
    
    # Создание цепочки
    chain = prompt | llm | StrOutputParser()
    
    print("=== Демонстрация асинхронных цепочек ===\n")
    
    # Асинхронный вызов
    print("1. Одиночный асинхронный вызов:")
    result = await chain.ainvoke({"topic": "искусственный интеллект"})
    print(f"Результат: {result}\n")
    
    # Параллельные вызовы
    print("2. Параллельные асинхронные вызовы:")
    topics = ["космос", "история", "технологии", "биология"]
    
    # Создаем задачи для параллельного выполнения
    tasks = [chain.ainvoke({"topic": topic}) for topic in topics]
    
    # Выполняем все задачи параллельно
    results = await asyncio.gather(*tasks)
    
    # Выводим результаты
    for topic, result in zip(topics, results):
        print(f"{topic.capitalize()}: {result}")
    
    print("\n=== Завершено ===")

def main():
    """Основная функция."""
    try:
        # Запуск асинхронной функции
        asyncio.run(async_chain_example())
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()