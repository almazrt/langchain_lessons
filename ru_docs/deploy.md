# Развертывание LangSmith

Когда вы готовы развернуть своего агента LangChain в продакшене, LangSmith предоставляет управляемую платформу хостинга, предназначенную для рабочих нагрузок агентов. Традиционные платформы хостинга созданы для безстатусных, краткосрочных веб-приложений, в то время как LangGraph **специально создан для статусных, долгосрочных агентов**, которые требуют постоянного состояния и фонового выполнения. LangSmith управляет инфраструктурой, масштабированием и операционными вопросами, так что вы можете развертывать прямо из вашего репозитория.

## Предварительные требования

Перед началом убедитесь, что у вас есть следующее:

* [Аккаунт GitHub](https://github.com/)
* [Аккаунт LangSmith](https://smith.langchain.com/) (бесплатная регистрация)

## Развертывание вашего агента

### 1. Создайте репозиторий на GitHub

Код вашего приложения должен находиться в репозитории GitHub для развертывания на LangSmith. Поддерживаются как публичные, так и частные репозитории. Для этого быстрого старта сначала убедитесь, что ваше приложение совместимо с LangGraph, следуя [руководству по настройке локального сервера](/oss/python/langchain/studio#setup-local-agent-server). Затем отправьте свой код в репозиторий.

### 2. Развертывание на LangSmith

<Steps>
  <Step title="Перейдите к развертываниям LangSmith">
    Войдите в [LangSmith](https://smith.langchain.com/). В левой боковой панели выберите **Deployments**.
  </Step>

  <Step title="Создайте новое развертывание">
    Нажмите кнопку **+ New Deployment**. Откроется панель, где вы можете заполнить необходимые поля.
  </Step>

  <Step title="Свяжите репозиторий">
    Если вы первый раз пользователь или добавляете частный репозиторий, который ранее не был подключен, нажмите кнопку **Add new account** и следуйте инструкциям для подключения вашего аккаунта GitHub.
  </Step>

  <Step title="Разверните репозиторий">
    Выберите репозиторий вашего приложения. Нажмите **Submit** для развертывания. Это может занять около 15 минут. Вы можете проверить статус в представлении **Deployment details**.
  </Step>
</Steps>

### 3. Протестируйте ваше приложение в Studio

После развертывания вашего приложения:

1. Выберите развертывание, которое вы только что создали, чтобы просмотреть больше деталей.
2. Нажмите кнопку **Studio** в правом верхнем углу. Studio откроется для отображения вашего графа.

### 4. Получите URL API для вашего развертывания

1. В представлении **Deployment details** в LangGraph нажмите **API URL**, чтобы скопировать его в буфер обмена.
2. Нажмите `URL`, чтобы скопировать его в буфер обмена.

### 5. Протестируйте API

Теперь вы можете протестировать API:

<Tabs>
  <Tab title="Python">
    1. Установите LangGraph Python:

    ```shell  theme={null}
    pip install langgraph-sdk
    ```

    2. Отправьте сообщение агенту:

    ```python  theme={null}
    from langgraph_sdk import get_sync_client # или get_client для асинхронного

    client = get_sync_client(url="your-deployment-url", api_key="your-langsmith-api-key")

    for chunk in client.runs.stream(
        None,    # Запуск без потока
        "agent", # Имя агента. Определено в langgraph.json.
        input={
            "messages": [{
                "role": "human",
                "content": "Что такое LangGraph?",
            }],
        },
        stream_mode="updates",
    ):
        print(f"Получение нового события типа: {chunk.event}...")
        print(chunk.data)
        print("\n\n")
    ```
  </Tab>

  <Tab title="Rest API">
    ```bash  theme={null}
    curl -s --request POST \
        --url <DEPLOYMENT_URL>/runs/stream \
        --header 'Content-Type: application/json' \
        --header "X-Api-Key: <LANGSMITH API KEY> \
        --data "{
            \"assistant_id\": \"agent\", `# Имя агента. Определено в langgraph.json.`
            \"input\": {
                \"messages\": [
                    {
                        \"role\": \"human\",
                        \"content\": \"Что такое LangGraph?\"
                    }
                ]
            },
            \"stream_mode\": \"updates\"
        }"
    ```
  </Tab>
</Tabs>

<Tip>
  LangSmith предлагает дополнительные варианты хостинга, включая самохостинг и гибридный. Для получения дополнительной информации см. [Обзор настройки платформы](/langsmith/platform-setup).
</Tip>

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/deploy.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt