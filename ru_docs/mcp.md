# Протокол контекста модели (MCP)

[Протокол контекста модели (MCP)](https://modelcontextprotocol.io/introduction) - это открытый протокол, который стандартизирует, как приложения предоставляют инструменты и контекст LLM. Агенты LangChain могут использовать инструменты, определенные на серверах MCP, используя библиотеку [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters).

## Установка

Установите библиотеку `langchain-mcp-adapters`, чтобы использовать инструменты MCP в LangGraph:

<CodeGroup>
  ```bash pip theme={null}
  pip install langchain-mcp-adapters
  ```

  ```bash uv theme={null}
  uv add langchain-mcp-adapters
  ```
</CodeGroup>

## Типы транспорта

MCP поддерживает различные механизмы транспорта для клиент-серверной связи:

* **stdio** – Клиент запускает сервер как подпроцесс и общается через стандартный ввод/вывод. Лучше всего подходит для локальных инструментов и простых настроек.
* **Потоковый HTTP** – Сервер работает как независимый процесс, обрабатывающий HTTP-запросы. Поддерживает удаленные соединения и несколько клиентов.
* **Server-Sent Events (SSE)** – вариант потокового HTTP, оптимизированный для связи в реальном времени.

## Использование инструментов MCP

`langchain-mcp-adapters` позволяет агентам использовать инструменты, определенные на одном или нескольких серверах MCP.

```python Доступ к нескольким серверам MCP icon="server" theme={null}
from langchain_mcp_adapters.client import MultiServerMCPClient  # [!code highlight]
from langchain.agents import create_agent


client = MultiServerMCPClient(  # [!code highlight]
    {
        "math": {
            "transport": "stdio",  # Локальная связь через подпроцесс
            "command": "python",
            # Абсолютный путь к вашему файлу math_server.py
            "args": ["/path/to/math_server.py"],
        },
        "weather": {
            "transport": "streamable_http",  # HTTP-базированный удаленный сервер
            # Убедитесь, что вы запустили ваш сервер погоды на порту 8000
            "url": "http://localhost:8000/mcp",
        }
    }
)

tools = await client.get_tools()  # [!code highlight]
agent = create_agent(
    "claude-sonnet-4-5-20250929",
    tools  # [!code highlight]
)
math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "чему равно (3 + 5) x 12?"}]}
)
weather_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "какая погода в Нью-Йорке?"}]}
)
```

<Note>
  `MultiServerMCPClient` **по умолчанию не имеет состояния**. Каждый вызов инструмента создает свежую MCP `ClientSession`, выполняет инструмент, а затем очищает.
</Note>

## Пользовательские серверы MCP

Чтобы создать свои собственные серверы MCP, вы можете использовать библиотеку `mcp`. Эта библиотека предоставляет простой способ определить [инструменты](https://modelcontextprotocol.io/docs/learn/server-concepts#tools-ai-actions) и запустить их как серверы.

<CodeGroup>
  ```bash pip theme={null}
  pip install mcp
  ```

  ```bash uv theme={null}
  uv add mcp
  ```
</CodeGroup>

Используйте следующие эталонные реализации для тестирования вашего агента с серверами инструментов MCP.

```python title="Сервер математики (транспорт stdio)" icon="floppy-disk" theme={null}
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Сложить два числа"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Умножить два числа"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

```python title="Сервер погоды (потоковый HTTP-транспорт)" icon="wifi" theme={null}
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Получить погоду для местоположения."""
    return "В Нью-Йорке всегда солнечно"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

## Использование инструментов с состоянием

Для серверов с состоянием, которые сохраняют контекст между вызовами инструментов, используйте `client.session()` для создания постоянной `ClientSession`.

```python Использование MCP ClientSession для использования инструментов с состоянием theme={null}
from langchain_mcp_adapters.tools import load_mcp_tools

client = MultiServerMCPClient({...})
async with client.session("math") as session:
    tools = await load_mcp_tools(session)
```

## Дополнительные ресурсы

* [Документация MCP](https://modelcontextprotocol.io/introduction)
* [Документация транспорта MCP](https://modelcontextprotocol.io/docs/concepts/transports)
* [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters)

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/mcp.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt