#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Мониторинг и логирование в LangChain
Этот пример демонстрирует использование callback handlers для мониторинга и логирования.
"""

import os
import logging
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CustomLoggingHandler(BaseCallbackHandler):
    """Пользовательский обработчик логирования."""
    
    def on_llm_start(self, serialized, prompts, **kwargs):
        logger.info(f"Начало вызова LLM с промптом: {prompts[0][:50]}...")
    
    def on_llm_end(self, response, **kwargs):
        logger.info(f"LLM вернул {len(response.generations)} вариантов ответа")
    
    def on_chain_start(self, serialized, inputs, **kwargs):
        logger.info(f"Начало выполнения цепочки с входными данными: {inputs}")
    
    def on_chain_end(self, outputs, **kwargs):
        logger.info(f"Цепочка завершена с выходными данными: {outputs}")
    
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get('name', 'Unknown')
        logger.info(f"Начало выполнения инструмента: {tool_name}")
    
    def on_tool_end(self, output, **kwargs):
        logger.info(f"Инструмент завершен с результатом: {output[:50]}...")

def monitoring_example():
    """Пример мониторинга и логирования."""
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
    prompt = ChatPromptTemplate.from_template("Ответь подробно на вопрос: {question}")
    
    # Создание цепочки
    chain = prompt | llm | StrOutputParser()
    
    print("=== Демонстрация мониторинга и логирования ===\n")
    
    # Создание обработчиков
    stdout_handler = StdOutCallbackHandler()
    custom_handler = CustomLoggingHandler()
    
    # Вызов цепочки с обработчиками
    print("Вызов цепочки с обработчиками логирования:")
    result = chain.invoke(
        {"question": "Что такое LangChain и зачем он нужен?"},
        config={"callbacks": [stdout_handler, custom_handler]}
    )
    
    print(f"\nФинальный результат:\n{result}")
    print("\n=== Завершено ===")

def main():
    """Основная функция."""
    try:
        monitoring_example()
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    main()