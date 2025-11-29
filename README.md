# Курс по изучению LangChain

Этот репозиторий содержит учебные материалы для изучения LangChain с нуля.

## Структура проекта

- [lessons/](lessons/) - теоретические материалы в формате Markdown
- [code/](code/) - практические примеры кода из уроков
- [requirements.txt](requirements.txt) - зависимости для запуска примеров

## Технические требования

- Python 3.x
- LangChain версия 1.1.0
- API ключи настроены через OpenRouter
- ОС: Kubuntu (или любая другая Linux система)

## Установка и настройка

1. Создайте виртуальное окружение:
   ```bash
   python3 -m venv langchain_env
   source langchain_env/bin/activate
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл .env и добавьте ваш API ключ:
   ```bash
   cp .env.example .env
   # Отредактируйте файл .env и добавьте ваш API ключ
   ```

## Уроки

1. [Урок 1: Введение в LangChain](lessons/lesson1.md) - основы работы с LangChain, создание первого приложения

## Язык материалов

Все уроки, комментарии и объяснения выполнены на русском языке.