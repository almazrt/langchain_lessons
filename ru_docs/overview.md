# Обзор LangChain

<Callout icon="bullhorn" color="#DFC5FE" iconType="regular">
  **LangChain v1.x теперь доступен-p ru_docs/middleware*

  Полный список изменений и инструкции по обновлению кода смотрите в [примечаниях к выпуску](/oss/python/releases/langchain-v1) и [руководстве по миграции](/oss/python/migrate/langchain-v1).

  Если вы столкнулись с какими-либо проблемами или у вас есть отзывы, пожалуйста, [сообщите о проблеме](https://github.com/langchain-ai/docs/issues/new?template=01-langchain.yml), чтобы мы могли улучшить продукт. Чтобы просмотреть документацию v0.x, [перейдите к архивному контенту](https://github.com/langchain-ai/langchain/tree/v0.3/docs/docs).
</Callout>

LangChain - это самый простой способ начать создавать агентов и приложения, работающие на базе LLM. Всего за 10 строк кода вы можете подключиться к OpenAI, Anthropic, Google и [другим](/oss/python/integrations/providers/overview). LangChain предоставляет готовую архитектуру агента и интеграции моделей, которые помогут вам быстро начать работу и без проблем внедрить LLM в ваших агентах и приложениях.

Мы рекомендуем использовать LangChain, если вы хотите быстро создавать агентов и автономные приложения. Используйте [LangGraph](/oss/python/langgraph/overview), наш низкоуровневый фреймворк и среду выполнения для оркестрации агентов, когда у вас есть более продвинутые потребности, требующие сочетания детерминированных и агентных рабочих процессов, значительной настройки и тщательно контролируемой задержки.

Агенты [LangChain](/oss/python/langchain/agents) построены поверх LangGraph для обеспечения надежного выполнения, потоковой передачи, участия человека в цикле, сохранения и многого другого. Вам не нужно знать LangGraph для базового использования агента LangChain.

## <Icon icon="wand-magic-sparkles" /> Создание агента

```python  theme={null}
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Получить погоду для указанного города."""

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="Вы полезный помощник",
)

# Запустить агента
agent.invoke(
    {"messages": [{"role": "user", "content": "какая погода в Сан-Франциско"}]}
)
```

Смотрите [Инструкции по установке](/oss/python/langchain/install) и [Краткое руководство](/oss/python/langchain/quickstart), чтобы начать создавать собственные агенты и приложения с помощью LangChain.

## <Icon icon="star" size={20} /> Основные преимущества

<Columns cols={2}>
  <Card title="Стандартный интерфейс модели" icon="arrows-rotate" href="/oss/python/langchain/models" arrow cta="Подробнее">
    Разные провайдеры имеют уникальные API для взаимодействия с моделями, включая формат ответов. LangChain стандартизирует то, как вы взаимодействуете с моделями, чтобы вы могли легко менять провайдеров и избежать привязки.
  </Card>

  <Card title="Простой в использовании, очень гибкий агент" icon="wand-magic-sparkles" href="/oss/python/langchain/agents" arrow cta="Подробнее">
    Абстракция агента LangChain разработана так, чтобы быть простой для начала работы, позволяя создать простого агента менее чем за 10 строк кода. Но она также обеспечивает достаточную гибкость, чтобы позволить вам делать всю контекстную инженерию, которую душа пожелает.
  </Card>

  <Card title="Построен на основе LangGraph" icon="circle-nodes" href="/oss/python/langgraph/overview" arrow cta="Подробнее">
    Агенты LangChain построены на основе LangGraph. Это позволяет нам воспользоваться преимуществами надежного выполнения LangGraph, поддержки участия человека в цикле, сохранения и многого другого.
  </Card>

  <Card title="Отладка с помощью LangSmith" icon="eye" href="/langsmith/home" arrow cta="Подробнее">
    Получите глубокую видимость сложного поведения агента с помощью инструментов визуализации, которые отслеживают пути выполнения, фиксируют переходы состояний и предоставляют подробные метрики времени выполнения.
  </Card>
</Columns>

***

<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/overview.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt
