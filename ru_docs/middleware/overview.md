# Обзор

> Контроль и настройка выполнения агента на каждом шагу

Промежуточное программное обеспечение (middleware) предоставляет способ более тесного контроля над тем, что происходит внутри агента. Промежуточное ПО полезно для следующего:

* Отслеживание поведения агента с помощью логирования, аналитики и отладки.
* Преобразование подсказок, [выбор инструментов](/oss/python/langchain/middleware/built-in#llm-tool-selector) и форматирование вывода.
* Добавление [повторных попыток](/oss/python/langchain/middleware/built-in#tool-retry), [резервных вариантов](/oss/python/langchain/middleware/built-in#model-fallback) и логики раннего прекращения.
* Применение [ограничений скорости](/oss/python/langchain/middleware/built-in#model-call-limit), защитных мер и [обнаружения PII](/oss/python/langchain/middleware/built-in#pii-detection).

Добавьте промежуточное ПО, передав их в [`create_agent`](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create_agent):

```python  theme={null}
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-4o",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...)
    ],
)
```

## Цикл агента

Основной цикл агента включает вызов модели, позволяя ей выбирать инструменты для выполнения, а затем завершение, когда она больше не вызывает инструменты:

<img src="https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=ac72e48317a9ced68fd1be64e89ec063" alt="Диаграмма основного цикла агента" style={{height: "200px", width: "auto", justifyContent: "center"}} className="rounded-lg block mx-auto" data-og-width="300" width="300" data-og-height="268" height="268" data-path="oss/images/core_agent_loop.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=280&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=a4c4b766b6678ef52a6ed556b1a0b032 280w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=560&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=111869e6e99a52c0eff60a1ef7ddc49c 560w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=840&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=6c1e21de7b53bd0a29683aca09c6f86e 840w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=1100&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=88bef556edba9869b759551c610c60f4 1100w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=1650&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=9b0bdd138e9548eeb5056dc0ed2d4a4b 1650w, https://mintcdn.com/langchain-5e9cc07a/Tazq8zGc0yYUYrDl/oss/images/core_agent_loop.png?w=2500&fit=max&auto=format&n=Tazq8zGc0yYUYrDl&q=85&s=41eb4f053ed5e6b0ba5bad2badf6d755 2500w" />

Промежуточное ПО предоставляет хуки до и после каждого из этих шагов:

<img src="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=eb4404b137edec6f6f0c8ccb8323eaf1" alt="Диаграмма потока промежуточного ПО" style={{height: "300px", width: "auto", justifyContent: "center"}} className="rounded-lg mx-auto" data-og-width="500" width="500" data-og-height="560" height="560" data-path="oss/images/middleware_final.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=280&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=483413aa87cf93323b0f47c0dd5528e8 280w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=560&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=41b7dd647447978ff776edafe5f42499 560w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=840&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=e9b14e264f68345de08ae76f032c52d4 840w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1100&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=ec45e1932d1279b1beee4a4b016b473f 1100w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=1650&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=3bca5ebf8aa56632b8a9826f7f112e57 1650w, https://mintcdn.com/langchain-5e9cc07a/RAP6mjwE5G00xYsA/oss/images/middleware_final.png?w=2500&fit=max&auto=format&n=RAP6mjwE5G00xYsA&q=85&s=437f141d1266f08a95f030c2804691d9 2500w" />

## Дополнительные ресурсы

<CardGroup cols={2}>
  <Card title="Встроенное промежуточное ПО" icon="box" href="/oss/python/langchain/middleware/built-in">
    Изучите встроенное промежуточное ПО для распространенных случаев использования.
  </Card>

  <Card title="Пользовательское промежуточное ПО" icon="code" href="/oss/python/langchain/middleware/custom">
    Создайте свое собственное промежуточное ПО с хуками и декораторами.
  </Card>

  <Card title="Справочник по API промежуточного ПО" icon="book" href="https://reference.langchain.com/python/langchain/middleware/">
    Полная справочная информация по API промежуточного ПО.
  </Card>

  <Card title="Тестирование агентов" icon="scale-unbalanced" href="/oss/python/langchain/test">
    Протестируйте своих агентов с помощью LangSmith.
  </Card>
</CardGroup>

***

<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/middleware/overview.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt
