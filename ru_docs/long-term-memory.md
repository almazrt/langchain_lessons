# Долгосрочная память

## Обзор

Агенты LangChain используют [сохранение LangGraph](/oss/python/langgraph/persistence#memory-store) для включения долгосрочной памяти. Это более продвинутая тема, требующая знаний LangGraph для использования.

## Хранение памяти

LangGraph хранит долгосрочные воспоминания как JSON-документы в [хранилище](/oss/python/langgraph/persistence#memory-store).

Каждое воспоминание организовано под пользовательским `namespace` (похожим на папку) и отдельным `key` (как имя файла). Пространства имен часто включают ID пользователя или организации или другие метки, которые облегчают организацию информации.

Эта структура обеспечивает иерархическую организацию воспоминаний. Поиск между пространствами имен поддерживается через фильтры контента.

```python  theme={null}
from langgraph.store.memory import InMemoryStore


def embed(texts: list[str]) -> list[list[float]]:
    # Замените на фактическую функцию встраивания или объект встраивания LangChain
    return [[1.0, 2.0] * len(texts)]


# InMemoryStore сохраняет данные в словарь в памяти. Используйте хранилище с поддержкой БД в производстве.
store = InMemoryStore(index={"embed": embed, "dims": 2}) # [!code highlight]
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context) # [!code highlight]
store.put( # [!code highlight]
    namespace,
    "a-memory",
    {
        "rules": [
            "Пользователю нравится короткий, прямой язык",
            "Пользователь говорит только на английском и python",
        ],
        "my-key": "my-value",
    },
)
# получить "воспоминание" по ID
item = store.get(namespace, "a-memory") # [!code highlight]
# поиск "воспоминаний" в этом пространстве имен, фильтрация по эквивалентности контента, сортировка по векторному сходству
items = store.search( # [!code highlight]
    namespace, filter={"my-key": "my-value"}, query="language preferences"
)
```

Для получения дополнительной информации о хранилище памяти см. руководство [Сохранение](/oss/python/langgraph/persistence#memory-store).

## Чтение долгосрочной памяти в инструментах

```python Инструмент, который агент может использовать для поиска информации о пользователе theme={null}
from dataclasses import dataclass

from langchain_core.runnables import RunnableConfig
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore


@dataclass
class Context:
    user_id: str

# InMemoryStore сохраняет данные в словарь в памяти. Используйте хранилище с поддержкой БД в производстве.
store = InMemoryStore() # [!code highlight]

# Запись образцов данных в хранилище с помощью метода put
store.put( # [!code highlight]
    ("users",),  # Пространство имен для группировки связанных данных вместе (пространство имен пользователей для данных пользователя)
    "user_123",  # Ключ в пространстве имен (ID пользователя как ключ)
    {
        "name": "John Smith",
        "language": "English",
    }  # Данные для хранения для данного пользователя
)

@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """Поиск информации о пользователе."""
    # Доступ к хранилищу - то же самое, что предоставлено в `create_agent`
    store = runtime.store # [!code highlight]
    user_id = runtime.context.user_id
    # Получение данных из хранилища - возвращает объект StoreValue со значением и метаданными
    user_info = store.get(("users",), user_id) # [!code highlight]
    return str(user_info.value) if user_info else "Неизвестный пользователь"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_user_info],
    # Передача хранилища агенту - позволяет агенту получать доступ к хранилищу при запуске инструментов
    store=store, # [!code highlight]
    context_schema=Context
)

# Запуск агента
agent.invoke(
    {"messages": [{"role": "user", "content": "найти информацию о пользователе"}]},
    context=Context(user_id="user_123") # [!code highlight]
)
```

<a id="write-long-term" />

## Запись долгосрочной памяти из инструментов

```python Пример инструмента, который обновляет информацию о пользователе theme={null}
from dataclasses import dataclass
from typing_extensions import TypedDict

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langgraph.store.memory import InMemoryStore


# InMemoryStore сохраняет данные в словарь в памяти. Используйте хранилище с поддержкой БД в производстве.
store = InMemoryStore() # [!code highlight]

@dataclass
class Context:
    user_id: str

# TypedDict определяет структуру информации о пользователе для LLM
class UserInfo(TypedDict):
    name: str

# Инструмент, который позволяет агенту обновлять информацию о пользователе (полезно для чат-приложений)
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    """Сохранение информации о пользователе."""
    # Доступ к хранилищу - то же самое, что предоставлено в `create_agent`
    store = runtime.store # [!code highlight]
    user_id = runtime.context.user_id # [!code highlight]
    # Хранение данных в хранилище (пространство имен, ключ, данные)
    store.put(("users",), user_id, user_info) # [!code highlight]
    return "Информация о пользователе успешно сохранена."

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[save_user_info],
    store=store, # [!code highlight]
    context_schema=Context
)

# Запуск агента
agent.invoke(
    {"messages": [{"role": "user", "content": "Меня зовут Джон Смит"}]},
    # user_id передается в контексте для идентификации, чья информация обновляется
    context=Context(user_id="user_123") # [!code highlight]
)

# Вы можете получить доступ к хранилищу напрямую для получения значения
store.get(("users",), "user_123").value
```

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/long-term-memory.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt