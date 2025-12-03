# Наблюдаемость LangSmith

При создании и запуске агентов с LangChain вам нужна возможность видеть, как они себя ведут: какие [инструменты](/oss/python/langchain/tools) они вызывают, какие подсказки генерируют и как принимают решения. Агенты LangChain, созданные с помощью [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent), автоматически поддерживают трассировку через [LangSmith](/langsmith/home) - платформу для захвата, отладки, оценки и мониторинга поведения приложений LLM.

[*Трассы*](/langsmith/observability-concepts#traces) записывают каждый шаг выполнения вашего агента, от начального пользовательского ввода до финального ответа, включая все вызовы инструментов, взаимодействия с моделью и точки принятия решений. Эти данные выполнения помогают вам отлаживать проблемы, оценивать производительность при различных входных данных и отслеживать шаблоны использования в продакшене.

Это руководство показывает, как включить трассировку для ваших агентов LangChain и использовать LangSmith для анализа их выполнения.

## Предварительные требования

Прежде чем начать, убедитесь, что у вас есть следующее:

* **Аккаунт LangSmith**: Зарегистрируйтесь (бесплатно) или войдите на [smith.langchain.com](https://smith.langchain.com).
* **API-ключ LangSmith**: Следуйте руководству [Создание API-ключа](/langsmith/create-account-api-key#create-an-api-key).

## Включение трассировки

Все агенты LangChain автоматически поддерживают трассировку LangSmith. Чтобы включить её, установите следующие переменные окружения:

```bash  theme={null}
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<ваш-api-ключ>
```

## Быстрый старт

Для регистрации трассировки в LangSmith не требуется дополнительного кода. Просто запустите код вашего агента, как обычно:

```python  theme={null}
from langchain.agents import create_agent


def send_email(to: str, subject: str, body: str):
    """Отправить электронное письмо получателю."""
    # ... логика отправки электронной почты
    return f"Письмо отправлено {to}"

def search_web(query: str):
    """Поиск информации в интернете."""
    # ... логика веб-поиска
    return f"Результаты поиска для: {query}"

agent = create_agent(
    model="gpt-4o",
    tools=[send_email, search_web],
    system_prompt="Вы полезный помощник, который может отправлять электронные письма и искать в интернете."
)

# Запустите агента - все шаги будут автоматически трассироваться
response = agent.invoke({
    "messages": [{"role": "user", "content": "Найдите последние новости об ИИ и отправьте краткое содержание на john@example.com"}]
})
```

По умолчанию трасса будет записана в проект с именем `default`. Чтобы настроить собственное имя проекта, см. [Запись в проект](#запись-в-проект).

## Селективная трассировка

Вы можете выбрать трассировку конкретных вызовов или частей вашего приложения, используя контекстный менеджер `tracing_context` LangSmith:

```python  theme={null}
import langsmith as ls

# Это БУДЕТ трассироваться
with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Отправьте тестовое письмо на alice@example.com"}]})

# Это НЕ будет трассироваться (если LANGSMITH_TRACING не установлен)
agent.invoke({"messages": [{"role": "user", "content": "Отправьте еще одно письмо"}]})
```

## Запись в проект

<Accordion title="Статически">
  Вы можете установить собственное имя проекта для всего вашего приложения, установив переменную окружения `LANGSMITH_PROJECT`:

  ```bash  theme={null}
  export LANGSMITH_PROJECT=my-agent-project
  ```
</Accordion>

<Accordion title="Динамически">
  Вы можете программно установить имя проекта для конкретных операций:

  ```python  theme={null}
  import langsmith as ls

  with ls.tracing_context(project_name="email-agent-test", enabled=True):
      response = agent.invoke({
          "messages": [{"role": "user", "content": "Отправьте приветственное письмо"}]
      })
  ```
</Accordion>

## Добавление метаданных в трассы

Вы можете аннотировать свои трассы пользовательскими метаданными и тегами:

```python  theme={null}
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Отправьте приветственное письмо"}]},
    config={
        "tags": ["production", "email-assistant", "v1.0"],
        "metadata": {
            "user_id": "user_123",
            "session_id": "session_456",
            "environment": "production"
        }
    }
)
```

`tracing_context` также принимает теги и метаданные для детального контроля:

```python  theme={null}
with ls.tracing_context(
    project_name="email-agent-test",
    enabled=True,
    tags=["production", "email-assistant", "v1.0"],
    metadata={"user_id": "user_123", "session_id": "session_456", "environment": "production"}):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "Отправьте приветственное письмо"}]}
    )
```

Эти пользовательские метаданные и теги будут прикреплены к трассе в LangSmith.

<Tip>
  Чтобы узнать больше о том, как использовать трассы для отладки, оценки и мониторинга ваших агентов, см. [документацию LangSmith](/langsmith/home).
</Tip>

***

<Callout icon="pen-to-square" iconType="regular">
  [Отредактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/observability.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>


---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt