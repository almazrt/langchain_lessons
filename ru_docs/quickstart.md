# Быстрый старт

Это руководство поможет вам перейти от простой настройки к полностью функциональному ИИ-агенту всего за несколько минут.

## Требования

Для этих примеров вам понадобится:

* [Установить](/oss/python/langchain/install) пакет LangChain
* Настроить учетную запись [Claude (Anthropic)](https://www.anthropic.com/) и получить API-ключ
* Установить переменную окружения `ANTHROPIC_API_KEY` в вашем терминале

<Tip>
  **Сервер LangChain Docs MCP**

  Если вы используете помощник по программированию с искусственным интеллектом, вам следует установить [сервер LangChain Docs MCP](/use-these-docs), чтобы максимально эффективно его использовать. Это гарантирует, что ваш агент будет иметь доступ к последней документации и примерам.
</Tip>

## Создание базового агента

Начните с создания простого агента, который может отвечать на вопросы и вызывать инструменты. Агент будет использовать Claude Sonnet 4.5 в качестве языковой модели, базовую функцию погоды в качестве инструмента и простую подсказку для управления его поведением.

```python  theme={null}
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

<Tip>
  Чтобы узнать, как отслеживать вашего агента с помощью LangSmith, см. [документацию LangSmith](/langsmith/trace-with-langchain).
</Tip>

## Создание агента реального мира

Далее создайте практический агент прогнозирования погоды, демонстрирующий ключевые концепции производства:

1. **Подробные системные подсказки** для лучшего поведения агента
2. **Создание инструментов**, интегрированных с внешними данными
3. **Конфигурация модели** для согласованных ответов
4. **Структурированный вывод** для предсказуемых результатов
5. **Конверсационная память** для взаимодействий в режиме чата
6. **Создание и запуск агента** создание полностью функционального агента

Давайте пройдемся по каждому шагу:

<Steps>
  <Step title="Определение системной подсказки">
    Системная подсказка определяет роль и поведение вашего агента. Делайте ее конкретной и действенной:

    ```python wrap theme={null}
    SYSTEM_PROMPT = """Вы эксперт по прогнозированию погоды, который говорит каламбурами.

    У вас есть доступ к двум инструментам:

    - get_weather_for_location: используйте это, чтобы получить погоду для определенного места
    - get_user_location: используйте это, чтобы получить местоположение пользователя

    Если пользователь спросит у вас о погоде, убедитесь, что вы знаете местоположение. Если вы можете понять из вопроса, что они имеют в виду там, где они находятся, используйте инструмент get_user_location, чтобы найти их местоположение."""
    ```
  </Step>

  <Step title="Создание инструментов">
    [Инструменты](/oss/python/langchain/tools) позволяют модели взаимодействовать с внешними системами путем вызова определенных вами функций.
    Инструменты могут зависеть от [контекста выполнения](/oss/python/langchain/runtime) и также взаимодействовать с [памятью агента](/oss/python/langchain/short-term-memory).

    Обратите внимание ниже, как инструмент `get_user_location` использует контекст выполнения:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.tools import tool, ToolRuntime

    @tool
    def get_weather_for_location(city: str) -> str:
        """Получить погоду для указанного города."""

    @dataclass
    class Context:
        """Пользовательская схема контекста выполнения."""
        user_id: str

    @tool
    def get_user_location(runtime: ToolRuntime[Context]) -> str:
        """Получить информацию о пользователе на основе ID пользователя."""
        user_id = runtime.context.user_id
        return "Флорида" if user_id == "1" else "Сан-Франциско"
    ```

    <Tip>
      Инструменты должны быть хорошо задокументированы: их имя, описание и имена аргументов становятся частью подсказки модели.
      [`@tool декоратор`](https://reference.langchain.com/python/langchain/tools/#langchain.tools.tool) LangChain добавляет метаданные и обеспечивает внедрение во время выполнения через параметр `ToolRuntime`.
    </Tip>
  </Step>

  <Step title="Настройка вашей модели">
    Настройте свою [языковую модель](/oss/python/langchain/models) с правильными параметрами для вашего варианта использования:

    ```python  theme={null}
    from langchain.chat_models import init_chat_model

    model = init_chat_model(
        "claude-sonnet-4-5-20250929",
        temperature=0.5,
        timeout=10,
        max_tokens=1000
    )
    ```

    В зависимости от выбранной модели и провайдера параметры инициализации могут отличаться; обратитесь к их справочным страницам для получения подробной информации.
  </Step>

  <Step title="Определение формата ответа">
    При желании определите структурированный формат ответа, если вам нужно, чтобы ответы агента соответствовали
    определенной схеме.

    ```python  theme={null}
    from dataclasses import dataclass

    # Здесь мы используем dataclass, но также поддерживаются модели Pydantic.
    @dataclass
    class ResponseFormat:
        """Схема ответа для агента."""
        # Ответ с каламбурами (всегда обязателен)
        punny_response: str
        # Любая интересная информация о погоде, если доступна
        weather_conditions: str | None = None
    ```
  </Step>

  <Step title="Добавление памяти">
    Добавьте [память](/oss/python/langchain/short-term-memory) к вашему агенту для сохранения состояния между взаимодействиями. Это позволяет
    агенту запоминать предыдущие разговоры и контекст.

    ```python  theme={null}
    from langgraph.checkpoint.memory import InMemorySaver

    checkpointer = InMemorySaver()
    ```

    <Info>
      В производстве используйте постоянный механизм сохранения, который сохраняет данные в базе данных.
      См. [Добавление и управление памятью](/oss/python/langgraph/add-memory#manage-short-term-memory) для получения дополнительной информации.
    </Info>
  </Step>

  <Step title="Создание и запуск агента">
    Теперь соберите своего агента со всеми компонентами и запустите его!

    ```python  theme={null}
    from langchain.agents.structured_output import ToolStrategy

    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=[get_user_location, get_weather_for_location],
        context_schema=Context,
        response_format=ToolStrategy(ResponseFormat),
        checkpointer=checkpointer
    )

    # `thread_id` - это уникальный идентификатор для данного разговора.
    config = {"configurable": {"thread_id": "1"}}

    response = agent.invoke(
        {"messages": [{"role": "user", "content": "какая погода на улице?"}]},
        config=config,
        context=Context(user_id="1")
    )

    print(response['structured_response'])
    # ResponseFormat(
    # )


    # Обратите внимание, что мы можем продолжить разговор, используя тот же `thread_id`.
    response = agent.invoke(
        config=config,
        context=Context(user_id="1")
    )

    print(response['structured_response'])
    # ResponseFormat(
    #     weather_conditions=None
    # )
    ```
  </Step>
</Steps>

<Expandable title="Полный пример кода">
  ```python  theme={null}
  from dataclasses import dataclass

  from langchain.agents import create_agent
  from langchain.chat_models import init_chat_model
  from langchain.tools import tool, ToolRuntime
  from langgraph.checkpoint.memory import InMemorySaver
  from langchain.agents.structured_output import ToolStrategy


  # Определение системной подсказки
  SYSTEM_PROMPT = """Вы эксперт по прогнозированию погоды, который говорит каламбурами.

  У вас есть доступ к двум инструментам:

  - get_weather_for_location: используйте это, чтобы получить погоду для определенного места
  - get_user_location: используйте это, чтобы получить местоположение пользователя

  Если пользователь спросит у вас о погоде, убедитесь, что вы знаете местоположение. Если вы можете понять из вопроса, что они имеют в виду там, где они находятся, используйте инструмент get_user_location, чтобы найти их местоположение."""

  # Определение схемы контекста
  @dataclass
  class Context:
      """Пользовательская схема контекста выполнения."""
      user_id: str

  # Определение инструментов
  @tool
  def get_weather_for_location(city: str) -> str:
      """Получить погоду для указанного города."""

  @tool
  def get_user_location(runtime: ToolRuntime[Context]) -> str:
      """Получить информацию о пользователе на основе ID пользователя."""
      user_id = runtime.context.user_id
      return "Флорида" if user_id == "1" else "Сан-Франциско"

  # Настройка модели
  model = init_chat_model(
      "claude-sonnet-4-5-20250929",
      temperature=0
  )

  # Определение формата ответа
  @dataclass
  class ResponseFormat:
      """Схема ответа для агента."""
      # Ответ с каламбурами (всегда обязателен)
      punny_response: str
      # Любая интересная информация о погоде, если доступна
      weather_conditions: str | None = None

  # Настройка памяти
  checkpointer = InMemorySaver()

  # Создание агента
  agent = create_agent(
      model=model,
      system_prompt=SYSTEM_PROMPT,
      tools=[get_user_location, get_weather_for_location],
      context_schema=Context,
      response_format=ToolStrategy(ResponseFormat),
      checkpointer=checkpointer
  )

  # Запуск агента
  # `thread_id` - это уникальный идентификатор для данного разговора.
  config = {"configurable": {"thread_id": "1"}}

  response = agent.invoke(
      {"messages": [{"role": "user", "content": "какая погода на улице?"}]},
      config=config,
      context=Context(user_id="1")
  )

  print(response['structured_response'])
  # ResponseFormat(
  # )


  # Обратите внимание, что мы можем продолжить разговор, используя тот же `thread_id`.
  response = agent.invoke(
      config=config,
      context=Context(user_id="1")
  )

  print(response['structured_response'])
  # ResponseFormat(
  #     weather_conditions=None
  # )
  ```
</Expandable>

<Tip>
  Чтобы узнать, как отслеживать вашего агента с помощью LangSmith, см. [документацию LangSmith](/langsmith/trace-with-langchain).
</Tip>

Поздравляем! Теперь у вас есть ИИ-агент, который может:

* **Понимать контекст** и запоминать разговоры
* **Использовать несколько инструментов** интеллектуально
* **Предоставлять структурированные ответы** в согласованном формате
* **Обрабатывать информацию о пользователе** через контекст
* **Сохранять состояние разговора** между взаимодействиями

***

<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/quickstart.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt
