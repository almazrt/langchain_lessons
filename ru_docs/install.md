# Установка LangChain

Чтобы установить пакет LangChain:

<CodeGroup>
  ```bash pip theme={null}
  pip install -U langchain
  # Требуется Python 3.10+
  ```

  ```bash uv theme={null}
  uv add langchain
  # Требуется Python 3.10+
  ```
</CodeGroup>

LangChain предоставляет интеграции со сотнями LLM и тысячами других интеграций. Они находятся в независимых пакетах провайдеров. Например:

<CodeGroup>
  ```bash pip theme={null}
  # Установка интеграции OpenAI
  pip install -U langchain-openai

  # Установка интеграции Anthropic
  pip install -U langchain-anthropic
  ```

  ```bash uv theme={null}
  # Установка интеграции OpenAI
  uv add langchain-openai

  # Установка интеграции Anthropic
  uv add langchain-anthropic
  ```
</CodeGroup>

<Tip>
  См. [вкладку Интеграции](/oss/python/integrations/providers/overview) для полного списка доступных интеграций.
</Tip>

***

<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/install.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt
