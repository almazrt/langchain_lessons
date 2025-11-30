#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обработка ошибок и отказоустойчивость в LangChain
Этот пример демонстрирует различные подходы к обработке ошибок в LangChain.
"""

import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from tenacity import retry, stop_after_attempt, wait_exponential

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_error(error: Exception) -> str:
    """Функция обработки ошибок."""
    logger.error(f"Произошла ошибка: {str(error)}")
    return "Извините, произошла ошибка при обработке запроса. Пожалуйста, попробуйте еще раз."

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def robust_llm_call(prompt, llm):
    """Вызов LLM с механизмом повторных попыток."""
    try:
        logger.info("Вызов LLM...")
        response = llm.invoke(prompt)
        logger.info("Вызов LLM успешен")
        return response
    except Exception as e:
        logger.warning(f"Ошибка при вызове LLM: {e}")
        raise  # Повторная попытка

def error_handling_example():
    """Пример обработки ошибок."""
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
    prompt = ChatPromptTemplate.from_template("Ответь на вопрос: {question}")
    
    # Создание цепочки без обработки ошибок
    chain = prompt | llm | StrOutputParser()
    
    print("=== Демонстрация обработки ошибок ===\n")
    
    # Пример нормального вызова
    print("1. Нормальный вызов:")
    try:
        result = chain.invoke({"question": "Что такое искусственный интеллект?"})
        print(f"Результат: {result}\n")
    except Exception as e:
        print(f"Ошибка: {str(e)}\n")
    
    # Создание цепочки с обработкой ошибок
    chain_with_fallback = (
        prompt 
        | llm 
        | StrOutputParser()
    ).with_fallbacks([RunnableLambda(handle_error)])
    
    print("2. Вызов с обработкой ошибок:")
    try:
        result = chain_with_fallback.invoke({"question": "Что такое машинное обучение?"})
        print(f"Результат: {result}\n")
    except Exception as e:
        print(f"Ошибка: {str(e)}\n")
    
    # Пример вызова с повторными попытками
    print("3. Вызов с повторными попытками:")
    try:
        result = robust_llm_call("Объясни концепцию нейронных сетей", llm)
        print(f"Результат: {result.content}\n")
    except Exception as e:
        print(f"Ошибка после всех повторных попыток: {str(e)}\n")
    
    print("=== Завершено ===")

def main():
    """Основная функция."""
    try:
        error_handling_example()
    except Exception as e:
        logger.error(f"Произошла ошибка в основном приложении: {str(e)}")

if __name__ == "__main__":
    main()