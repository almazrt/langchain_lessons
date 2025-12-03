# Контекстное проектирование в агентах

## Обзор

### Почему агенты терпят неудачу?

Когда агенты терпят неудачу, это обычно происходит потому, что вызов LLM внутри агента выполнил неправильное действие или не сделал того, чего мы ожидали. LLM могут терпеть неудачу по одной из двух причин:

1. Базовая LLM недостаточно способна
2. Правильный контекст не был передан LLM

Чаще всего причиной ненадежности агентов является вторая причина.

**Контекстное проектирование** — это предоставление правильной информации и инструментов в нужном формате, чтобы LLM могла выполнить задачу. Это главная задача AI-инженеров. Отсутствие "правильного" контекста является основным препятствием для более надежных агентов, и абстракции агентов LangChain специально разработаны для облегчения контекстного проектирования.

<Tip>
Новичок в контекстном проектировании? Начните с [концептуального обзора](/oss/python/concepts/context), чтобы понять различные типы контекста и когда их использовать.
</Tip>

### Цикл агента

Типичный цикл агента состоит из двух основных шагов:

1. **Вызов модели** - вызывает LLM с подсказкой и доступными инструментами, возвращает либо ответ, либо запрос на выполнение инструментов
2. **Выполнение инструмента** - выполняет инструменты, запрошенные LLM, возвращает результаты инструментов

<div style={{ display: "flex", justifyContent: "center" }}>
  <img src="https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=ac72e48317a9ced68fd1be64e89ec063" alt="Диаграмма основного цикла агента" className="rounded-lg" data-og-width="300" width="300" data-og-height="268" height="268" data-path="oss/images/core_agent_loop.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=280&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=a4c4b766b6678ef52a6ed556b1a0b032 280w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=560&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=111869e6e99a52c0eff60a1ef7ddc49c 560w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=840&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=6c1e21de7b53bd0a29683aca09c6f86e 840w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=1100&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=88bef556edba9869b759551c610c60f4 1100w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=1650&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=9b0bdd138e9548eeb5056dc0ed2d4a4b 1650w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=2500&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=41eb4f053ed5e6b0ba5bad2badf6d755 2500w" />
</div>

Этот цикл продолжается до тех пор, пока LLM не решит завершить работу.

### Что вы можете контролировать

Чтобы создавать надежных агентов, вам нужно контролировать то, что происходит на каждом этапе цикла агента, а также то, что происходит между этапами.

| Тип контекста                                  | Что вы контролируете                                                                     | Временный или постоянный |
| --------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------- |
| **[Контекст модели](#контекст-модели)**           | Что попадает в вызовы модели (инструкции, история сообщений, инструменты, формат ответа)   | Временный               |
| **[Контекст инструмента](#контекст-инструмента)**             | Доступ и производство инструментов (чтение/запись состояния, хранилища, контекста времени выполнения)    | Постоянный              |
| **[Контекст жизненного цикла](#контекст-жизненного-цикла)** | Что происходит между вызовами модели и инструмента (обобщение, защитные механизмы, ведение журнала и т.д.) | Постоянный              |

<CardGroup>
  <Card title="Временный контекст" icon="bolt" iconType="duotone">
    То, что LLM видит для одного вызова. Вы можете изменять сообщения, инструменты или подсказки без изменения того, что сохранено в состоянии.
  </Card>

  <Card title="Постоянный контекст" icon="database" iconType="duotone">
    То, что сохраняется в состоянии между ходами. Хуки жизненного цикла и записи инструментов изменяют это постоянно.
  </Card>
</CardGroup>

### Источники данных

На протяжении этого процесса ваш агент получает доступ (читает / записывает) к различным источникам данных:

| Источник данных         | Также известен как        | Область применения               | Примеры                                                                   |
| ------------------- | -------------------- | ------------------- | -------------------------------------------------------------------------- |
| **Контекст времени выполнения** | Статическая конфигурация | Область беседы | ID пользователя, ключи API, соединения с базой данных, разрешения, настройки среды |
| **Состояние**           | Краткосрочная память    | Область беседы | Текущие сообщения, загруженные файлы, статус аутентификации, результаты инструментов      |
| **Хранилище**           | Долгосрочная память     | Межбеседование  | Предпочтения пользователей, извлеченные идеи, воспоминания, исторические данные            |

### Как это работает

[Промежуточное ПО](/oss/python/langchain/middleware) LangChain - это механизм, который делает контекстное проектирование практичным для разработчиков, использующих LangChain.

Промежуточное ПО позволяет вам подключаться к любому шагу в жизненном цикле агента и:

* Обновлять контекст
* Переходить к другому шагу в жизненном цикле агента

На протяжении этого руководства вы будете часто видеть использование API промежуточного ПО как средства достижения целей контекстного проектирования.

## Контекст модели

Управляйте тем, что попадает в каждый вызов модели - инструкции, доступные инструменты, какую модель использовать и формат вывода. Эти решения напрямую влияют на надежность и стоимость.

<CardGroup cols={2}>
  <Card title="Системная подсказка" icon="message-lines" href="#системная-подсказка">
    Базовые инструкции от разработчика к LLM.
  </Card>

  <Card title="Сообщения" icon="comments" href="#сообщения">
    Полный список сообщений (история беседы), отправленных в LLM.
  </Card>

  <Card title="Инструменты" icon="wrench" href="#инструменты">
    Утилиты, к которым имеет доступ агент для выполнения действий.
  </Card>

  <Card title="Модель" icon="brain-circuit" href="#модель">
    Фактическая модель (включая конфигурацию), которая будет вызвана.
  </Card>

  <Card title="Формат ответа" icon="brackets-curly" href="#формат-ответа">
    Спецификация схемы для окончательного ответа модели.
  </Card>
</CardGroup>

Все эти типы контекста модели могут черпать информацию из **состояния** (краткосрочной памяти), **хранилища** (долгосрочной памяти) или **контекста времени выполнения** (статической конфигурации).

### Системная подсказка

Системная подсказка устанавливает поведение и возможности LLM. Разные пользователи, контексты или этапы беседы требуют разных инструкций. Успешные агенты используют воспоминания, предпочтения и конфигурацию для предоставления правильных инструкций для текущего состояния беседы.

<Tabs>
  <Tab title="Состояние">
    Доступ к количеству сообщений или контексту беседы из состояния:

    ```python  theme={null}
    from langchain.agents import create_agent
    from langchain.agents.middleware import dynamic_prompt, ModelRequest

    @dynamic_prompt
    def state_aware_prompt(request: ModelRequest) -> str:
        # request.messages - это ярлык для request.state["messages"]
        message_count = len(request.messages)

        base = "Вы полезный помощник."

        if message_count > 10:
            base += "\nЭто длинная беседа - будьте особенно кратки."

        return base

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[state_aware_prompt]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Доступ к предпочтениям пользователя из долгосрочной памяти:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import dynamic_prompt, ModelRequest
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    @dynamic_prompt
    def store_aware_prompt(request: ModelRequest) -> str:
        user_id = request.runtime.context.user_id

        # Чтение из хранилища: получить предпочтения пользователя
        store = request.runtime.store
        user_prefs = store.get(("preferences",), user_id)

        base = "Вы полезный помощник."

        if user_prefs:
            style = user_prefs.value.get("communication_style", "balanced")
            base += f"\nПользователь предпочитает {style} ответы."

        return base

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[store_aware_prompt],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Доступ к ID пользователя или конфигурации из контекста времени выполнения:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import dynamic_prompt, ModelRequest

    @dataclass
    class Context:
        user_role: str
        deployment_env: str

    @dynamic_prompt
    def context_aware_prompt(request: ModelRequest) -> str:
        # Чтение из контекста времени выполнения: роль пользователя и среда
        user_role = request.runtime.context.user_role
        env = request.runtime.context.deployment_env

        base = "Вы полезный помощник."

        if user_role == "admin":
            base += "\nУ вас есть права администратора. Вы можете выполнять все операции."
        elif user_role == "viewer":
            base += "\nУ вас есть права только на чтение. Руководите пользователями только к операциям чтения."

        if env == "production":
            base += "\nБудьте особенно осторожны при изменении данных."

        return base

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[context_aware_prompt],
        context_schema=Context
    )
    ```
  </Tab>
</Tabs>

### Сообщения

Сообщения составляют подсказку, которая отправляется в LLM.
Критически важно управлять содержимым сообщений, чтобы обеспечить LLM правильной информацией для хорошего ответа.

<Tabs>
  <Tab title="Состояние">
    Внедрение контекста загруженных файлов из состояния, когда это актуально для текущего запроса:

    ```python  theme={null}
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable

    @wrap_model_call
    def inject_file_context(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Внедрение контекста о файлах, загруженных пользователем в этой сессии."""
        # Чтение из состояния: получить метаданные загруженных файлов
        uploaded_files = request.state.get("uploaded_files", [])  # [!code highlight]

        if uploaded_files:
            # Создание контекста о доступных файлах
            file_descriptions = []
            for file in uploaded_files:
                file_descriptions.append(
                    f"- {file['name']} ({file['type']}): {file['summary']}"
                )

            file_context = f"""Файлы, к которым у вас есть доступ в этой беседе:
    {chr(10).join(file_descriptions)}

    Ссылайтесь на эти файлы при ответах на вопросы."""
            # Внедрение контекста файла перед последними сообщениями
            messages = [  # [!code highlight]
                *request.messages,
                {"role": "user", "content": file_context},
            ]
            request = request.override(messages=messages)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[inject_file_context]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Внедрение стиля написания электронных писем пользователя из хранилища для руководства созданию:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    @wrap_model_call
    def inject_writing_style(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Внедрение стиля написания электронных писем пользователя из хранилища."""
        user_id = request.runtime.context.user_id  # [!code highlight]

        # Чтение из хранилища: получить примеры стиля написания пользователя
        store = request.runtime.store  # [!code highlight]
        writing_style = store.get(("writing_style",), user_id)  # [!code highlight]

        if writing_style:
            style = writing_style.value
            # Создание руководства по стилю из сохраненных примеров
            style_context = f"""Ваш стиль написания:
    - Тон: {style.get('tone', 'профессиональный')}
    - Типичное приветствие: "{style.get('greeting', 'Привет')}"
    - Типичное завершение: "{style.get('sign_off', 'С наилучшими пожеланиями')}"
    - Пример электронного письма, которое вы написали:
    {style.get('example_email', '')}"""

            # Добавление в конце - модели больше внимания уделяют последним сообщениям
            messages = [
                *request.messages,
                {"role": "user", "content": style_context}
            ]
            request = request.override(messages=messages)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[inject_writing_style],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Внедрение правил соответствия из контекста времени выполнения на основе юрисдикции пользователя:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable

    @dataclass
    class Context:
        user_jurisdiction: str
        industry: str
        compliance_frameworks: list[str]

    @wrap_model_call
    def inject_compliance_rules(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Внедрение ограничений соответствия из контекста времени выполнения."""
        # Чтение из контекста времени выполнения: получить требования соответствия
        jurisdiction = request.runtime.context.user_jurisdiction  # [!code highlight]
        industry = request.runtime.context.industry  # [!code highlight]
        frameworks = request.runtime.context.compliance_frameworks  # [!code highlight]

        # Создание ограничений соответствия
        rules = []
        if "GDPR" in frameworks:
            rules.append("- Необходимо получить явное согласие перед обработкой персональных данных")
            rules.append("- У пользователей есть право на удаление данных")
        if "HIPAA" in frameworks:
            rules.append("- Нельзя делиться медицинской информацией пациента без авторизации")
            rules.append("- Необходимо использовать безопасную, зашифрованную связь")
        if industry == "finance":
            rules.append("- Нельзя предоставлять финансовые советы без надлежащих отказов от ответственности")

        if rules:
            compliance_context = f"""Требования соответствия для {jurisdiction}:
    {chr(10).join(rules)}"""

            # Добавление в конце - модели больше внимания уделяют последним сообщениям
            messages = [
                *request.messages,
                {"role": "user", "content": compliance_context}
            ]
            request = request.override(messages=messages)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[inject_compliance_rules],
        context_schema=Context
    )
    ```
  </Tab>
</Tabs>

<Note>
  **Временные против постоянных обновлений сообщений:**

  Примеры выше используют `wrap_model_call` для создания **временных** обновлений - изменения того, какие сообщения отправляются модели для одного вызова без изменения того, что сохранено в состоянии.

  Для **постоянных** обновлений, которые изменяют состояние (например, пример обобщения в [Контексте жизненного цикла](#обобщение)), используйте хуки жизненного цикла, такие как `before_model` или `after_model`, чтобы постоянно обновлять историю беседы. Смотрите [документацию по промежуточному ПО](/oss/python/langchain/middleware) для получения дополнительной информации.
</Note>

### Инструменты

Инструменты позволяют модели взаимодействовать с базами данных, API и внешними системами. То, как вы определяете и выбираете инструменты, напрямую влияет на то, сможет ли модель эффективно выполнять задачи.

#### Определение инструментов

Каждый инструмент нуждается в четком имени, описании, именах аргументов и описаниях аргументов. Это не просто метаданные - они направляют рассуждение модели о том, когда и как использовать инструмент.

```python  theme={null}
from langchain.tools import tool

@tool(parse_docstring=True)
def search_orders(
    user_id: str,
    status: str,
    limit: int = 10
) -> str:
    """Поиск заказов пользователя по статусу.

    Используйте это, когда пользователь спрашивает об истории заказов или хочет проверить
    статус заказа. Всегда фильтруйте по предоставленному статусу.

    Args:
        user_id: Уникальный идентификатор пользователя
        status: Статус заказа: 'pending', 'shipped', или 'delivered'
        limit: Максимальное количество результатов для возврата
    """
    # Реализация здесь
    pass
```

#### Выбор инструментов

Не каждый инструмент подходит для каждой ситуации. Слишком много инструментов может перегрузить модель (перегрузить контекст) и увеличить количество ошибок; слишком мало ограничивает возможности. Динамический выбор инструментов адаптирует доступный набор инструментов на основе состояния аутентификации, разрешений пользователя, флагов функций или этапа беседы.

<Tabs>
  <Tab title="Состояние">
    Включение расширенных инструментов только после определенных этапов беседы:

    ```python  theme={null}
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable

    @wrap_model_call
    def state_based_tools(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Фильтрация инструментов на основе состояния беседы."""
        # Чтение из состояния: проверка, аутентифицирован ли пользователь
        state = request.state  # [!code highlight]
        is_authenticated = state.get("authenticated", False)  # [!code highlight]
        message_count = len(state["messages"])

        # Включение чувствительных инструментов только после аутентификации
        if not is_authenticated:
            tools = [t for t in request.tools if t.name.startswith("public_")]
            request = request.override(tools=tools)  # [!code highlight]
        elif message_count < 5:
            # Ограничение инструментов на ранних этапах беседы
            tools = [t for t in request.tools if t.name != "advanced_search"]
            request = request.override(tools=tools)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[public_search, private_search, advanced_search],
        middleware=[state_based_tools]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Фильтрация инструментов на основе предпочтений пользователя или флагов функций в хранилище:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    @wrap_model_call
    def store_based_tools(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Фильтрация инструментов на основе предпочтений в хранилище."""
        user_id = request.runtime.context.user_id

        # Чтение из хранилища: получить включенные функции пользователя
        store = request.runtime.store
        feature_flags = store.get(("features",), user_id)

        if feature_flags:
            enabled_features = feature_flags.value.get("enabled_tools", [])
            # Включение только инструментов, доступных для этого пользователя
            tools = [t for t in request.tools if t.name in enabled_features]
            request = request.override(tools=tools)

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[search_tool, analysis_tool, export_tool],
        middleware=[store_based_tools],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Фильтрация инструментов на основе разрешений пользователя из контекста времени выполнения:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from typing import Callable

    @dataclass
    class Context:
        user_role: str

    @wrap_model_call
    def context_based_tools(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Фильтрация инструментов на основе разрешений контекста времени выполнения."""
        # Чтение из контекста времени выполнения: получить роль пользователя
        user_role = request.runtime.context.user_role

        if user_role == "admin":
            # Администраторы получают все инструменты
            pass
        elif user_role == "editor":
            # Редакторы не могут удалять
            tools = [t for t in request.tools if t.name != "delete_data"]
            request = request.override(tools=tools)
        else:
            # Просмотрщики получают инструменты только для чтения
            tools = [t for t in request.tools if t.name.startswith("read_")]
            request = request.override(tools=tools)

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[read_data, write_data, delete_data],
        middleware=[context_based_tools],
        context_schema=Context
    )
    ```
  </Tab>
</Tabs>

Смотрите [Динамический выбор инструментов](/oss/python/langchain/middleware#динамический-выбор-инструментов) для получения дополнительных примеров.

### Модель

Разные модели имеют разные сильные стороны, стоимости и контекстные окна. Выберите правильную модель для задачи, которая
может меняться во время выполнения агента.

<Tabs>
  <Tab title="Состояние">
    Использование разных моделей на основе длины беседы из состояния:

    ```python  theme={null}
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from langchain.chat_models import init_chat_model
    from typing import Callable

    # Инициализация моделей один раз вне промежуточного ПО
    large_model = init_chat_model("claude-sonnet-4-5-20250929")
    standard_model = init_chat_model("gpt-4o")
    efficient_model = init_chat_model("gpt-4o-mini")

    @wrap_model_call
    def state_based_model(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор модели на основе длины беседы в состоянии."""
        # request.messages - это ярлык для request.state["messages"]
        message_count = len(request.messages)  # [!code highlight]

        if message_count > 20:
            # Длинная беседа - использование модели с большим контекстным окном
            model = large_model
        elif message_count > 10:
            # Средняя беседа
            model = standard_model
        else:
            # Короткая беседа - использование эффективной модели
            model = efficient_model

        request = request.override(model=model)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o-mini",
        tools=[...],
        middleware=[state_based_model]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Использование предпочтительной модели пользователя из хранилища:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from langchain.chat_models import init_chat_model
    from typing import Callable
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    # Инициализация доступных моделей один раз
    MODEL_MAP = {
        "gpt-4o": init_chat_model("gpt-4o"),
        "gpt-4o-mini": init_chat_model("gpt-4o-mini"),
        "claude-sonnet": init_chat_model("claude-sonnet-4-5-20250929"),
    }

    @wrap_model_call
    def store_based_model(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор модели на основе предпочтений в хранилище."""
        user_id = request.runtime.context.user_id

        # Чтение из хранилища: получить предпочтительную модель пользователя
        store = request.runtime.store
        user_prefs = store.get(("preferences",), user_id)

        if user_prefs:
            preferred_model = user_prefs.value.get("preferred_model")
            if preferred_model and preferred_model in MODEL_MAP:
                request = request.override(model=MODEL_MAP[preferred_model])

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[store_based_model],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Выбор модели на основе лимитов стоимости или среды из контекста времени выполнения:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from langchain.chat_models import init_chat_model
    from typing import Callable

    @dataclass
    class Context:
        cost_tier: str
        environment: str

    # Инициализация моделей один раз вне промежуточного ПО
    premium_model = init_chat_model("claude-sonnet-4-5-20250929")
    standard_model = init_chat_model("gpt-4o")
    budget_model = init_chat_model("gpt-4o-mini")

    @wrap_model_call
    def context_based_model(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор модели на основе контекста времени выполнения."""
        # Чтение из контекста времени выполнения: уровень стоимости и среда
        cost_tier = request.runtime.context.cost_tier
        environment = request.runtime.context.environment

        if environment == "production" and cost_tier == "premium":
            # Премиум-пользователи в продакшене получают лучшую модель
            model = premium_model
        elif cost_tier == "budget":
            # Уровень бюджета получает эффективную модель
            model = budget_model
        else:
            # Стандартный уровень
            model = standard_model

        request = request.override(model=model)

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[context_based_model],
        context_schema=Context
    )
    ```
  </Tab>
</Tabs>

Смотрите [Динамическая модель](/oss/python/langchain/agents#динамическая-модель) для получения дополнительных примеров.

### Формат ответа

Структурированный вывод преобразует неструктурированный текст в проверенные, структурированные данные. При извлечении конкретных полей или возврате данных для систем нижнего уровня свободная форма текста недостаточна.

**Как это работает:** Когда вы предоставляете схему в качестве формата ответа, окончательный ответ модели гарантированно будет соответствовать этой схеме. Агент выполняет цикл вызова модели/инструментов до тех пор, пока модель не закончит вызывать инструменты, затем окончательный ответ приводится к предоставленному формату.

#### Определение форматов

Определения схем направляют модель. Имена полей, типы и описания точно указывают, какому формату должен соответствовать вывод.

```python  theme={null}
from pydantic import BaseModel, Field

class CustomerSupportTicket(BaseModel):
    """Структурированная информация о заявке, извлеченная из сообщения клиента."""

    category: str = Field(
        description="Категория проблемы: 'billing', 'technical', 'account', или 'product'"
    )
    priority: str = Field(
        description="Уровень срочности: 'low', 'medium', 'high', или 'critical'"
    )
    summary: str = Field(
        description="Краткое описание проблемы клиента в одно предложение"
    )
    customer_sentiment: str = Field(
        description="Эмоциональный тон клиента: 'frustrated', 'neutral', или 'satisfied'"
    )
```

#### Выбор форматов

Динамический выбор формата ответа адаптирует схемы на основе предпочтений пользователя, этапа беседы или роли - возвращая простые форматы на ранних этапах и подробные форматы по мере увеличения сложности.

<Tabs>
  <Tab title="Состояние">
    Настройка структурированного вывода на основе состояния беседы:

    ```python  theme={null}
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from pydantic import BaseModel, Field
    from typing import Callable

    class SimpleResponse(BaseModel):
        """Простой ответ для ранней беседы."""
        answer: str = Field(description="Краткий ответ")

    class DetailedResponse(BaseModel):
        """Подробный ответ для установленной беседы."""
        answer: str = Field(description="Подробный ответ")
        reasoning: str = Field(description="Объяснение рассуждений")
        confidence: float = Field(description="Оценка уверенности 0-1")

    @wrap_model_call
    def state_based_output(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор формата вывода на основе состояния."""
        # request.messages - это ярлык для request.state["messages"]
        message_count = len(request.messages)  # [!code highlight]

        if message_count < 3:
            # Ранняя беседа - использование простого формата
            request = request.override(response_format=SimpleResponse)  # [!code highlight]
        else:
            # Установленная беседа - использование подробного формата
            request = request.override(response_format=DetailedResponse)  # [!code highlight]

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[state_based_output]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Настройка формата вывода на основе предпочтений пользователя в хранилище:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from pydantic import BaseModel, Field
    from typing import Callable
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    class VerboseResponse(BaseModel):
        """Подробный ответ с деталями."""
        answer: str = Field(description="Подробный ответ")
        sources: list[str] = Field(description="Использованные источники")

    class ConciseResponse(BaseModel):
        """Краткий ответ."""
        answer: str = Field(description="Краткий ответ")

    @wrap_model_call
    def store_based_output(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор формата вывода на основе предпочтений в хранилище."""
        user_id = request.runtime.context.user_id

        # Чтение из хранилища: получить предпочтительный стиль ответа пользователя
        store = request.runtime.store
        user_prefs = store.get(("preferences",), user_id)

        if user_prefs:
            style = user_prefs.value.get("response_style", "concise")
            if style == "verbose":
                request = request.override(response_format=VerboseResponse)
            else:
                request = request.override(response_format=ConciseResponse)

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[store_based_output],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Настройка формата вывода на основе контекста времени выполнения, такого как роль пользователя или среда:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
    from pydantic import BaseModel, Field
    from typing import Callable

    @dataclass
    class Context:
        user_role: str
        environment: str

    class AdminResponse(BaseModel):
        """Ответ с техническими деталями для администраторов."""
        answer: str = Field(description="Ответ")
        debug_info: dict = Field(description="Отладочная информация")
        system_status: str = Field(description="Статус системы")

    class UserResponse(BaseModel):
        """Простой ответ для обычных пользователей."""
        answer: str = Field(description="Ответ")

    @wrap_model_call
    def context_based_output(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse]
    ) -> ModelResponse:
        """Выбор формата вывода на основе контекста времени выполнения."""
        # Чтение из контекста времени выполнения: роль пользователя и среда
        user_role = request.runtime.context.user_role
        environment = request.runtime.context.environment

        if user_role == "admin" and environment == "production":
            # Администраторы в продакшене получают подробный вывод
            request = request.override(response_format=AdminResponse)
        else:
            # Обычные пользователи получают простой вывод
            request = request.override(response_format=UserResponse)

        return handler(request)

    agent = create_agent(
        model="gpt-4o",
        tools=[...],
        middleware=[context_based_output],
        context_schema=Context
    )
    ```
  </Tab>
</Tabs>

## Контекст инструмента

Инструменты особенные, потому что они одновременно читают и записывают контекст.

В самом базовом случае, когда инструмент выполняется, он получает параметры запроса LLM и возвращает сообщение инструмента обратно. Инструмент выполняет свою работу и производит результат.

Инструменты также могут извлекать важную информацию для модели, которая позволяет ей выполнять и завершать задачи.

### Чтения

Большинству реальных инструментов нужно больше, чем просто параметры LLM. Им нужны ID пользователей для запросов к базе данных, ключи API для внешних сервисов или текущее состояние сессии для принятия решений. Инструменты читают из состояния, хранилища и контекста времени выполнения для доступа к этой информации.

<Tabs>
  <Tab title="Состояние">
    Чтение из состояния для проверки информации текущей сессии:

    ```python  theme={null}
    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent

    @tool
    def check_authentication(
        runtime: ToolRuntime
    ) -> str:
        """Проверка аутентификации пользователя."""
        # Чтение из состояния: проверка текущего статуса аутентификации
        current_state = runtime.state
        is_authenticated = current_state.get("authenticated", False)

        if is_authenticated:
            return "Пользователь аутентифицирован"
        else:
            return "Пользователь не аутентифицирован"

    agent = create_agent(
        model="gpt-4o",
        tools=[check_authentication]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Чтение из хранилища для доступа к сохраненным предпочтениям пользователя:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    @tool
    def get_preference(
        preference_key: str,
        runtime: ToolRuntime[Context]
    ) -> str:
        """Получение предпочтения пользователя из хранилища."""
        user_id = runtime.context.user_id

        # Чтение из хранилища: получение существующих предпочтений
        store = runtime.store
        existing_prefs = store.get(("preferences",), user_id)

        if existing_prefs:
            value = existing_prefs.value.get(preference_key)
            return f"{preference_key}: {value}" if value else f"Нет установленного предпочтения для {preference_key}"
        else:
            return "Предпочтения не найдены"

    agent = create_agent(
        model="gpt-4o",
        tools=[get_preference],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>

  <Tab title="Контекст времени выполнения">
    Чтение из контекста времени выполнения для конфигурации, такой как ключи API и ID пользователей:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent

    @dataclass
    class Context:
        user_id: str
        api_key: str
        db_connection: str

    @tool
    def fetch_user_data(
        query: str,
        runtime: ToolRuntime[Context]
    ) -> str:
        """Получение данных с использованием конфигурации контекста времени выполнения."""
        # Чтение из контекста времени выполнения: получение ключа API и соединения с БД
        user_id = runtime.context.user_id
        api_key = runtime.context.api_key
        db_connection = runtime.context.db_connection

        # Использование конфигурации для получения данных
        results = perform_database_query(db_connection, query, api_key)

        return f"Найдено {len(results)} результатов для пользователя {user_id}"

    agent = create_agent(
        model="gpt-4o",
        tools=[fetch_user_data],
        context_schema=Context
    )

    # Вызов с контекстом времени выполнения
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Получить мои данные"}]},
        context=Context(
            user_id="user_123",
            api_key="sk-...",
            db_connection="postgresql://..."
        )
    )
    ```
  </Tab>
</Tabs>

### Записи

Результаты инструментов могут использоваться для помощи агенту в выполнении данной задачи. Инструменты могут как возвращать результаты непосредственно в модель,
так и обновлять память агента, чтобы сделать важный контекст доступным для будущих шагов.

<Tabs>
  <Tab title="Состояние">
    Запись в состояние для отслеживания информации, специфичной для сессии, с использованием команды:

    ```python  theme={null}
    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent
    from langgraph.types import Command

    @tool
    def authenticate_user(
        password: str,
        runtime: ToolRuntime
    ) -> Command:
        """Аутентификация пользователя и обновление состояния."""
        # Выполнение аутентификации (упрощено)
        if password == "correct":
            # Запись в состояние: отметка как аутентифицированный с использованием команды
            return Command(
                update={"authenticated": True},
            )
        else:
            return Command(update={"authenticated": False})

    agent = create_agent(
        model="gpt-4o",
        tools=[authenticate_user]
    )
    ```
  </Tab>

  <Tab title="Хранилище">
    Запись в хранилище для сохранения данных между сессиями:

    ```python  theme={null}
    from dataclasses import dataclass
    from langchain.tools import tool, ToolRuntime
    from langchain.agents import create_agent
    from langgraph.store.memory import InMemoryStore

    @dataclass
    class Context:
        user_id: str

    @tool
    def save_preference(
        preference_key: str,
        preference_value: str,
        runtime: ToolRuntime[Context]
    ) -> str:
        """Сохранение предпочтения пользователя в хранилище."""
        user_id = runtime.context.user_id

        # Чтение существующих предпочтений
        store = runtime.store
        existing_prefs = store.get(("preferences",), user_id)

        # Объединение с новым предпочтением
        prefs = existing_prefs.value if existing_prefs else {}
        prefs[preference_key] = preference_value

        # Запись в хранилище: сохранение обновленных предпочтений
        store.put(("preferences",), user_id, prefs)

        return f"Сохранено предпочтение: {preference_key} = {preference_value}"

    agent = create_agent(
        model="gpt-4o",
        tools=[save_preference],
        context_schema=Context,
        store=InMemoryStore()
    )
    ```
  </Tab>
</Tabs>

Смотрите [Инструменты](/oss/python/langchain/tools) для комплексных примеров доступа к состоянию, хранилищу и контексту времени выполнения в инструментах.

## Контекст жизненного цикла

Контролируйте то, что происходит **между** основными шагами агента - перехватывайте поток данных для реализации сквозных задач, таких как обобщение, защитные механизмы и ведение журнала.

Как вы видели в [Контексте модели](#контекст-модели) и [Контексте инструмента](#контекст-инструмента), [промежуточное ПО](/oss/python/langchain/middleware) - это механизм, который делает контекстное проектирование практичным. Промежуточное ПО позволяет вам подключаться к любому шагу в жизненном цикле агента и либо:

1. **Обновлять контекст** - Изменять состояние и хранилище для сохранения изменений, обновлять историю беседы или сохранять идеи
2. **Переходить в жизненном цикле** - Переходить к другим шагам в цикле агента на основе контекста (например, пропустить выполнение инструмента, если условие выполнено, повторить вызов модели с измененным контекстом)

<div style={{ display: "flex", justifyContent: "center" }}>
  <img src="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=eb4404b137edec6f6f0c8ccb8323eaf1" alt="Хуки промежуточного ПО в цикле агента" className="rounded-lg" data-og-width="500" width="500" data-og-height="560" height="560" data-path="oss/images/middleware_final.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=280&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=483413aa87cf93323b0f47c0dd5528e8 280w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=560&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=41b7dd647447978ff776edafe5f42499 560w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=840&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=e9b14e264f68345de08ae76f032c52d4 840w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1100&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=ec45e1932d1279b1beee4a4b016b473f 1100w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1650&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=3bca5ebf8aa56632b8a9826f7f112e57 1650w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=2500&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=437f141d1266f08a95f030c2804691d9 2500w" />
</div>

### Пример: Обобщение

Одним из самых распространенных паттернов жизненного цикла является автоматическое сжатие истории беседы, когда она становится слишком длинной. В отличие от временной обрезки сообщений, показанной в [Контексте модели](#сообщения), обобщение **постоянно обновляет состояние** - навсегда заменяя старые сообщения обобщением, которое сохраняется для всех будущих ходов.

LangChain предлагает встроенное промежуточное ПО для этого:

```python  theme={null}
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger={"tokens": 4000},
            keep={"messages": 20},
        ),
    ],
)
```

Когда беседа превышает лимит токенов, `SummarizationMiddleware` автоматически:

1. Обобщает старые сообщения с помощью отдельного вызова LLM
2. Заменяет их сообщением обобщения в состоянии (постоянно)
3. Сохраняет последние сообщения нетронутыми для контекста

Обобщенная история беседы постоянно обновляется - будущие ходы будут видеть обобщение вместо оригинальных сообщений.

<Note>
  Для полного списка встроенного промежуточного ПО, доступных хуков и создания пользовательского промежуточного ПО см. [Документацию по промежуточному ПО](/oss/python/langchain/middleware).
</Note>

## Лучшие практики

1. **Начинайте просто** - Начинайте со статических подсказок и инструментов, добавляйте динамику только при необходимости
2. **Тестируйте постепенно** - Добавляйте одну функцию контекстного проектирования за раз
3. **Следите за производительностью** - Отслеживайте вызовы модели, использование токенов и задержки
4. **Используйте встроенное промежуточное ПО** - Используйте [`SummarizationMiddleware`](/oss/python/langchain/middleware#обобщение), [`LLMToolSelectorMiddleware`](/oss/python/langchain/middleware#селектор-инструментов-llm) и т.д.
5. **Документируйте свою стратегию контекста** - Ясно указывайте, какой контекст передается и почему
6. **Понимайте временное против постоянного**: Изменения контекста модели являются временными (на вызов), в то время как изменения контекста жизненного цикла сохраняются в состоянии

## Связанные ресурсы

* [Концептуальный обзор контекста](/oss/python/concepts/context) - Понимание типов контекста и когда их использовать
* [Промежуточное ПО](/oss/python/langchain/middleware) - Полное руководство по промежуточному ПО
* [Инструменты](/oss/python/langchain/tools) - Создание инструментов и доступ к контексту
* [Память](/oss/python/concepts/memory) - Паттерны краткосрочной и долгосрочной памяти
* [Агенты](/oss/python/langchain/agents) - Основные концепции агентов

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/context-engineering.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt