#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовые импорты для Lesson 5
Этот файл проверяет, что все необходимые библиотеки могут быть импортированы правильно.
"""

def test_imports():
    """Тест импортов для Lesson 5."""
    try:
        # Основные импорты LangChain
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnableLambda
        print("✓ Основные компоненты LangChain импортированы успешно")
        
        # Импорты для асинхронного программирования
        import asyncio
        print("✓ asyncio импортирован успешно")
        
        # Импорты для обработки ошибок
        from tenacity import retry, stop_after_attempt, wait_exponential
        print("✓_tenacity (retry) импортирован успешно")
        
        # Импорты для кэширования
        from langchain_core.globals import set_llm_cache
        from langchain_community.cache import InMemoryCache
        print("✓ Кэширование LangChain импортировано успешно")
        
        # Импорты для мониторинга
        from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler
        print("✓ Callback handlers импортированы успешно")
        
        # Импорты для конфигурации
        from dotenv import load_dotenv
        print("✓ dotenv импортирован успешно")
        
        print("\n✅ Все импорты успешно пройдены!")
        return True
        
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False

def main():
    """Основная функция."""
    print("=== Тестирование импортов для Lesson 5 ===\n")
    success = test_imports()
    
    if success:
        print("\n🎉 Готово! Все необходимые библиотеки установлены корректно.")
        print("Вы можете запускать примеры кода из этого урока.")
    else:
        print("\n⚠️ Обнаружены проблемы с импортами.")
        print("Пожалуйста, проверьте установку необходимых библиотек.")

if __name__ == "__main__":
    main()