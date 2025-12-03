# Защитные механизмы

> Реализация проверок безопасности и фильтрации контента для ваших агентов

Защитные механизмы помогают создавать безопасные, соответствующие требованиям AI-приложения путем проверки и фильтрации контента в ключевых точках выполнения вашего агента. Они могут обнаруживать конфиденциальную информацию, обеспечивать соблюдение политик контента, проверять выходные данные и предотвращать небезопасное поведение до возникновения проблем.

Общие случаи использования включают:

* Предотвращение утечки PII (персональных данных)
* Обнаружение и блокирование атак внедрения подсказок
* Блокирование неприемлемого или вредного контента
* Обеспечение соблюдения бизнес-правил и требований соответствия
* Проверка качества и точности выходных данных

Вы можете реализовать защитные механизмы с помощью [промежуточного ПО](/oss/python/langchain/middleware) для перехвата выполнения в стратегических точках - до начала работы агента, после его завершения или вокруг вызовов модели и инструментов.

<div style={{ display: "flex", justifyContent: "center" }}>
  <img src="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=eb4404b137edec6f6f0c8ccb8323eaf1" alt="Диаграмма потока промежуточного ПО" className="rounded-lg" data-og-width="500" width="500" data-og-height="560" height="560" data-path="oss/images/middleware_final.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=280&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=483413aa87cf93323b0f47c0dd5528e8 280w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=560&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=41b7dd647447978ff776edafe5f42499 560w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=840&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=e9b14e264f68345de08ae76f032c52d4 840w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1100&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=ec45e1932d1279b1beee4a4b016b473f 1100w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1650&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=3bca5ebf8aa56632b8a9826f7f112e57 1650w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=2500&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=437f141d1266f08a95f030c2804691d9 2500w" />
</div>

Защитные механизмы можно реализовать с помощью двух дополнительных подходов:

<CardGroup cols={2}>
  <Card title="Детерминированные защитные механизмы" icon="list-check">
    Использование логики на основе правил, таких как шаблоны регулярных выражений, сопоставление ключевых слов или явные проверки. Быстро, предсказуемо и экономично, но может пропустить нюансовые нарушения.
  </Card>

  <Card title="Основанные на модели защитные механизмы" icon="brain">
    Использование LLM или классификаторов для оценки контента с семантическим пониманием. Выявляют тонкие проблемы, которые правила пропускают, но работают медленнее и дороже.
  </Card>
</CardGroup>

LangChain предоставляет как встроенные защитные механизмы (например, [обнаружение PII](#обнаружение-pii), [человек-в-цикле](#человек-в-цикле)), так и гибкую систему промежуточного ПО для создания пользовательских защитных механизмов с использованием любого из этих подходов.

## Встроенные защитные механизмы

### Обнаружение PII

LangChain предоставляет встроенное промежуточное ПО для обнаружения и обработки Персональных Данных (PII) в беседах. Это промежуточное ПО может обнаруживать общие типы PII, такие как электронные адреса, кредитные карты, IP-адреса и другие.

Промежуточное ПО для обнаружения PII полезно для случаев, таких как медицинские и финансовые приложения с требованиями соответствия, агенты службы поддержки клиентов, которым необходимо очищать журналы, и вообще любые приложения, обрабатывающие конфиденциальные пользовательские данные.

Промежуточное ПО PII поддерживает несколько стратегий обработки обнаруженных PII:

| Стратегия | Описание                             | Пример               |
| -------- | --------------------------------------- | --------------------- |
| `redact` | Замена на `[REDACTED_TYPE]`          | `[REDACTED_EMAIL]`    |
| `mask`   | Частичное скрытие (например, последние 4 цифры) | `****-****-****-1234` |
| `hash`   | Замена на детерминированный хэш         | `a8f5f167...`         |
| `block`  | Вызов исключения при обнаружении           | Ошибка возникает          |

```python  theme={null}
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware


agent = create_agent(
    model="gpt-4o",
    tools=[customer_service_tool, email_tool],
    middleware=[
        # Редактирование электронных адресов во входных данных пользователя перед отправкой в модель
        PIIMiddleware(
            "email",
            strategy="redact",
            apply_to_input=True,
        ),
        # Маскирование кредитных карт во входных данных пользователя
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_input=True,
        ),
        # Блокировка API-ключей - вызов ошибки при обнаружении
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)

# Когда пользователь предоставляет PII, она будет обработана в соответствии со стратегией
result = agent.invoke({
    "messages": [{"role": "user", "content": "Мой электронный адрес john.doe@example.com и карта 5105-1051-0510-5100"}]
})
```

<Accordion title="Встроенные типы PII и конфигурация">
  **Встроенные типы PII:**

  * `email` - Электронные адреса
  * `credit_card` - Номера кредитных карт (проверка по алгоритму Луна)
  * `ip` - IP-адреса
  * `mac_address` - MAC-адреса
  * `url` - URL-адреса

  **Параметры конфигурации:**

  | Параметр               | Описание                                                            | По умолчанию                |
  | ----------------------- | ---------------------------------------------------------------------- | ---------------------- |
  | `pii_type`              | Тип PII для обнаружения (встроенный или пользовательский)                             | Обязательный               |
  | `strategy`              | Как обрабатывать обнаруженные PII (`"block"`, `"redact"`, `"mask"`, `"hash"`) | `"redact"`             |
  | `detector`              | Пользовательская функция обнаружения или шаблон регулярного выражения                              | `None` (используется встроенный) |
  | `apply_to_input`        | Проверка сообщений пользователя перед вызовом модели                                  | `True`                 |
  | `apply_to_output`       | Проверка сообщений ИИ после вызова модели                                     | `False`                |
  | `apply_to_tool_results` | Проверка сообщений результатов инструментов после выполнения                             | `False`                |
</Accordion>

Смотрите [документацию по промежуточному ПО](/oss/python/langchain/middleware#обнаружение-pii) для получения полной информации о возможностях обнаружения PII.

### Человек-в-цикле

LangChain предоставляет встроенное промежуточное ПО для требующего одобрения человека перед выполнением чувствительных операций. Это один из самых эффективных защитных механизмов для решений с высокими ставками.

Промежуточное ПО человек-в-цикле полезно для случаев, таких как финансовые транзакции и переводы, удаление или изменение производственных данных, отправка коммуникаций внешним сторонам и любые операции с значительным бизнес-влиянием.

```python  theme={null}
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command


agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, send_email_tool, delete_database_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                # Требовать одобрения для чувствительных операций
                "send_email": True,
                "delete_database": True,
                # Автоматическое одобрение безопасных операций
                "search": False,
            }
        ),
    ],
    # Сохранение состояния между прерываниями
    checkpointer=InMemorySaver(),
)

# Человек-в-цикле требует ID потока для сохранения
config = {"configurable": {"thread_id": "some_id"}}

# Агент приостановится и будет ждать одобрения перед выполнением чувствительных инструментов
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Отправить электронное письмо команде"}]},
    config=config
)

result = agent.invoke(
    Command(resume={"decisions": [{"type": "approve"}]}),
    config=config  # Тот же ID потока для возобновления приостановленной беседы
)
```

<Tip>
  Смотрите [документацию по человеку-в-цикле](/oss/python/langchain/human-in-the-loop) для получения полной информации о реализации рабочих процессов одобрения.
</Tip>

## Пользовательские защитные механизмы

Для более сложных защитных механизмов вы можете создать пользовательское промежуточное ПО, которое выполняется до или после выполнения агента. Это дает вам полный контроль над логикой проверки, фильтрацией контента и проверками безопасности.

### Защитные механизмы до агента

Используйте хуки "до агента" для однократной проверки запросов в начале каждого вызова. Это полезно для проверок на уровне сессии, таких как аутентификация, ограничение скорости или блокирование неприемлемых запросов до начала любой обработки.

<CodeGroup>
  ```python title="Синтаксис класса" theme={null}
  from typing import Any

  from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
  from langgraph.runtime import Runtime

  class ContentFilterMiddleware(AgentMiddleware):
      """Детерминированный защитный механизм: Блокирование запросов, содержащих запрещенные ключевые слова."""

      def __init__(self, banned_keywords: list[str]):
          super().__init__()
          self.banned_keywords = [kw.lower() for kw in banned_keywords]

      @hook_config(can_jump_to=["end"])
      def before_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
          # Получение первого сообщения пользователя
          if not state["messages"]:
              return None

          first_message = state["messages"][0]
          if first_message.type != "human":
              return None

          content = first_message.content.lower()

          # Проверка на запрещенные ключевые слова
          for keyword in self.banned_keywords:
              if keyword in content:
                  # Блокирование выполнения до начала любой обработки
                  return {
                      "messages": [{
                          "role": "assistant",
                          "content": "Я не могу обрабатывать запросы, содержащие неприемлемый контент. Пожалуйста, переформулируйте свой запрос."
                      }],
                      "jump_to": "end"
                  }

          return None

  # Использование пользовательского защитного механизма
  from langchain.agents import create_agent

  agent = create_agent(
      model="gpt-4o",
      tools=[search_tool, calculator_tool],
      middleware=[
          ContentFilterMiddleware(
              banned_keywords=["hack", "exploit", "malware"]
          ),
      ],
  )

  # Этот запрос будет заблокирован до начала любой обработки
  result = agent.invoke({
      "messages": [{"role": "user", "content": "Как мне взломать базу данных?"}]
  })
  ```

  ```python title="Синтаксис декоратора" theme={null}
  from typing import Any

  from langchain.agents.middleware import before_agent, AgentState, hook_config
  from langgraph.runtime import Runtime

  banned_keywords = ["hack", "exploit", "malware"]

  @before_agent(can_jump_to=["end"])
  def content_filter(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
      """Детерминированный защитный механизм: Блокирование запросов, содержащих запрещенные ключевые слова."""
      # Получение первого сообщения пользователя
      if not state["messages"]:
          return None

      first_message = state["messages"][0]
      if first_message.type != "human":
          return None

      content = first_message.content.lower()

      # Проверка на запрещенные ключевые слова
      for keyword in banned_keywords:
          if keyword in content:
              # Блокирование выполнения до начала любой обработки
              return {
                  "messages": [{
                      "role": "assistant",
                      "content": "Я не могу обрабатывать запросы, содержащие неприемлемый контент. Пожалуйста, переформулируйте свой запрос."
                  }],
                  "jump_to": "end"
              }

      return None

  # Использование пользовательского защитного механизма
  from langchain.agents import create_agent

  agent = create_agent(
      model="gpt-4o",
      tools=[search_tool, calculator_tool],
      middleware=[content_filter],
  )

  # Этот запрос будет заблокирован до начала любой обработки
  result = agent.invoke({
      "messages": [{"role": "user", "content": "Как мне взломать базу данных?"}]
  })
  ```
</CodeGroup>

### Защитные механизмы после агента

Используйте хуки "после агента" для проверки окончательных выходных данных перед возвратом пользователю. Это полезно для основанных на модели проверок безопасности, проверки качества или окончательных сканирований соответствия на полный ответ агента.

<CodeGroup>
  ```python title="Синтаксис класса" theme={null}
  from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
  from langgraph.runtime import Runtime
  from langchain.messages import AIMessage
  from langchain.chat_models import init_chat_model
  from typing import Any

  class SafetyGuardrailMiddleware(AgentMiddleware):
      """Основанный на модели защитный механизм: Использование LLM для оценки безопасности ответа."""

      def __init__(self):
          super().__init__()
          self.safety_model = init_chat_model("gpt-4o-mini")

      @hook_config(can_jump_to=["end"])
      def after_agent(self, state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
          # Получение окончательного ответа ИИ
          if not state["messages"]:
              return None

          last_message = state["messages"][-1]
          if not isinstance(last_message, AIMessage):
              return None

          # Использование модели для оценки безопасности
          safety_prompt = f"""Оцените, является ли этот ответ безопасным и подходящим.
          Отвечайте только 'SAFE' или 'UNSAFE'.

          Ответ: {last_message.content}"""

          result = self.safety_model.invoke([{"role": "user", "content": safety_prompt}])

          if "UNSAFE" in result.content:
              last_message.content = "Я не могу предоставить этот ответ. Пожалуйста, переформулируйте свой запрос."

          return None

  # Использование защитного механизма безопасности
  from langchain.agents import create_agent

  agent = create_agent(
      model="gpt-4o",
      tools=[search_tool, calculator_tool],
      middleware=[SafetyGuardrailMiddleware()],
  )

  result = agent.invoke({
      "messages": [{"role": "user", "content": "Как мне изготовить взрывчатые вещества?"}]
  })
  ```

  ```python title="Синтаксис декоратора" theme={null}
  from langchain.agents.middleware import after_agent, AgentState, hook_config
  from langgraph.runtime import Runtime
  from langchain.messages import AIMessage
  from langchain.chat_models import init_chat_model
  from typing import Any

  safety_model = init_chat_model("gpt-4o-mini")

  @after_agent(can_jump_to=["end"])
  def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
      """Основанный на модели защитный механизм: Использование LLM для оценки безопасности ответа."""
      # Получение окончательного ответа ИИ
      if not state["messages"]:
          return None

      last_message = state["messages"][-1]
      if not isinstance(last_message, AIMessage):
          return None

      # Использование модели для оценки безопасности
      safety_prompt = f"""Оцените, является ли этот ответ безопасным и подходящим.
      Отвечайте только 'SAFE' или 'UNSAFE'.

      Ответ: {last_message.content}"""

      result = safety_model.invoke([{"role": "user", "content": safety_prompt}])

      if "UNSAFE" in result.content:
          last_message.content = "Я не могу предоставить этот ответ. Пожалуйста, переформулируйте свой запрос."

      return None

  # Использование защитного механизма безопасности
  from langchain.agents import create_agent

  agent = create_agent(
      model="gpt-4o",
      tools=[search_tool, calculator_tool],
      middleware=[safety_guardrail],
  )

  result = agent.invoke({
      "messages": [{"role": "user", "content": "Как мне изготовить взрывчатые вещества?"}]
  })
  ```
</CodeGroup>

### Комбинирование нескольких защитных механизмов

Вы можете объединить несколько защитных механизмов, добавив их в массив промежуточного ПО. Они выполняются по порядку, позволяя создать многоуровневую защиту:

```python  theme={null}
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[search_tool, send_email_tool],
    middleware=[
        # Уровень 1: Детерминированный фильтр входных данных (до агента)
        ContentFilterMiddleware(banned_keywords=["hack", "exploit"]),

        # Уровень 2: Защита PII (до и после модели)
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("email", strategy="redact", apply_to_output=True),

        # Уровень 3: Одобрение человека для чувствительных инструментов
        HumanInTheLoopMiddleware(interrupt_on={"send_email": True}),

        # Уровень 4: Основанная на модели проверка безопасности (после агента)
        SafetyGuardrailMiddleware(),
    ],
)
```

## Дополнительные ресурсы

* [Документация по промежуточному ПО](/oss/python/langchain/middleware) - Полное руководство по пользовательскому промежуточному ПО
* [Справочник по API промежуточного ПО](https://reference.langchain.com/python/langchain/middleware/) - Полное руководство по пользовательскому промежуточному ПО
* [Человек-в-цикле](/oss/python/langchain/human-in-the-loop) - Добавление человеческого обзора для чувствительных операций
* [Тестирование агентов](/oss/python/langchain/test) - Стратегии тестирования механизмов безопасности

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/guardrails.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt