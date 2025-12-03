# Сообщения

Сообщения являются фундаментальной единицей контекста для моделей в LangChain. Они представляют собой входные и выходные данные моделей, неся как содержание, так и метаданные, необходимые для представления состояния беседы при взаимодействии с LLM.

Объекты сообщений содержат:

* <Icon icon="user" size={16} /> [**Роль**](#типы-сообщений) - Идентифицирует тип сообщения (например, `system`, `user`)
* <Icon icon="folder-closed" size={16} /> [**Содержание**](#содержание-сообщения) - Представляет фактическое содержание сообщения (например, текст, изображения, аудио, документы и т.д.)
* <Icon icon="tag" size={16} /> [**Метаданные**](#метаданные-сообщения) - Необязательные поля, такие как информация об ответе, ID сообщений и использование токенов

LangChain предоставляет стандартный тип сообщения, который работает со всеми поставщиками моделей, обеспечивая согласованное поведение независимо от вызываемой модели.

## Основное использование

Самый простой способ использования сообщений - создать объекты сообщений и передать их модели при [вызове](/oss/python/langchain/models#invocation).

```python  theme={null}
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("gpt-5-nano")

system_msg = SystemMessage("Вы полезный помощник.")
human_msg = HumanMessage("Здравствуйте, как вы?")
# Использование с чат-моделями
messages = [system_msg, human_msg]
response = model.invoke(messages)  # Возвращает AIMessage
```

### Текстовые подсказки

Текстовые подсказки - это строки - идеальны для простых задач генерации, когда вам не нужно сохранять историю беседы.

```python  theme={null}
response = model.invoke("Напишите хайку о весне")
```

**Используйте текстовые подсказки, когда:**

* У вас есть один, самостоятельный запрос
* Вам не нужна история беседы
* Вы хотите минимальной сложности кода

### Сообщения-подсказки

В качестве альтернативы вы можете передать модели список сообщений, предоставив список объектов сообщений.

```python  theme={null}
from langchain.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage("Вы эксперт по поэзии"),
    HumanMessage("Напишите хайку о весне"),
    AIMessage("Цветут вишневые деревья...")
]
response = model.invoke(messages)
```

**Используйте сообщения-подсказки, когда:**

* Управление многократными беседами
* Работа с мультимодальным контентом (изображения, аудио, файлы)
* Включение системных инструкций

### Формат словаря

Вы также можете указать сообщения непосредственно в формате завершения чата OpenAI.

```python  theme={null}
messages = [
    {"role": "system", "content": "Вы эксперт по поэзии"},
    {"role": "user", "content": "Напишите хайку о весне"},
    {"role": "assistant", "content": "Цветут вишневые деревья..."}
]
response = model.invoke(messages)
```

## Типы сообщений

* <Icon icon="gear" size={16} /> [Системное сообщение](#системное-сообщение) - Сообщает модели, как вести себя и предоставляет контекст для взаимодействий
* <Icon icon="user" size={16} /> [Человеческое сообщение](#человеческое-сообщение) - Представляет пользовательский ввод и взаимодействия с моделью
* <Icon icon="robot" size={16} /> [AI-сообщение](#ai-сообщение) - Ответы, сгенерированные моделью, включая текстовое содержание, вызовы инструментов и метаданные
* <Icon icon="wrench" size={16} /> [Сообщение инструмента](#сообщение-инструмента) - Представляет выходные данные [вызовов инструментов](/oss/python/langchain/models#tool-calling)

### Системное сообщение

[`SystemMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.SystemMessage) представляет начальный набор инструкций, который задает поведение модели. Вы можете использовать системное сообщение для установки тона, определения роли модели и установки рекомендаций для ответов.

```python Базовые инструкции theme={null}
system_msg = SystemMessage("Вы полезный помощник по программированию.")

messages = [
    system_msg,
    HumanMessage("Как создать REST API?")
]
response = model.invoke(messages)
```

```python Детализированная персона theme={null}
from langchain.messages import SystemMessage, HumanMessage

system_msg = SystemMessage("""
Вы опытный разработчик Python с экспертизой в веб-фреймворках.
Всегда предоставляйте примеры кода и объясняйте свои рассуждения.
Будьте кратки, но подробны в своих объяснениях.
""")

messages = [
    system_msg,
    HumanMessage("Как создать REST API?")
]
response = model.invoke(messages)
```

***

### Человеческое сообщение

[`HumanMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.HumanMessage) представляет пользовательский ввод и взаимодействия. Они могут содержать текст, изображения, аудио, файлы и любое количество мультимодального [содержания](#содержание-сообщения).

#### Текстовое содержание

<CodeGroup>
  ```python Объект сообщения theme={null}
  response = model.invoke([
    HumanMessage("Что такое машинное обучение?")
  ])
  ```

  ```python Строковый ярлык theme={null}
  # Использование строки - это ярлык для одного HumanMessage
  response = model.invoke("Что такое машинное обучение?")
  ```
</CodeGroup>

#### Метаданные сообщения

```python Добавление метаданных theme={null}
human_msg = HumanMessage(
    content="Здравствуйте!",
    name="alice",  # Необязательно: идентификация разных пользователей
    id="msg_123",  # Необязательно: уникальный идентификатор для трассировки
)
```

<Note>
  Поведение поля `name` различается в зависимости от поставщика - некоторые используют его для идентификации пользователей, другие игнорируют. Чтобы проверить, обратитесь к [справке](https://reference.langchain.com/python/integrations/) поставщика модели.
</Note>

***

### AI-сообщение

[`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) представляет выходные данные вызова модели. Они могут включать мультимодальные данные, вызовы инструментов и метаданные, специфичные для поставщика, к которым вы можете получить доступ позже.

```python  theme={null}
response = model.invoke("Объясните ИИ")
print(type(response))  # <class 'langchain.messages.AIMessage'>
```

Объекты [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) возвращаются моделью при ее вызове, что содержит все связанные метаданные в ответе.

Поставщики по-разному взвешивают/контекстуализируют типы сообщений, что означает, что иногда полезно вручную создать новый объект [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) и вставить его в историю сообщений, как если бы он пришел от модели.

```python  theme={null}
from langchain.messages import AIMessage, SystemMessage, HumanMessage

# Создание AI-сообщения вручную (например, для истории беседы)
ai_msg = AIMessage("Я буду рад помочь вам с этим вопросом!")

# Добавление в историю беседы
messages = [
    SystemMessage("Вы полезный помощник"),
    HumanMessage("Можете мне помочь?"),
    ai_msg,  # Вставка, как если бы она пришла от модели
    HumanMessage("Отлично! Сколько будет 2+2?")
]

response = model.invoke(messages)
```

<Accordion title="Атрибуты">
  <ParamField path="text" type="string">
    Текстовое содержание сообщения.
  </ParamField>

  <ParamField path="content" type="string | dict[]">
    Необработанное содержание сообщения.
  </ParamField>

  <ParamField path="content_blocks" type="ContentBlock[]">
    Стандартизированные [блоки содержания](#содержание-сообщения) сообщения.
  </ParamField>

  <ParamField path="tool_calls" type="dict[] | None">
    Вызовы инструментов, сделанные моделью.

    Пусто, если инструменты не вызываются.
  </ParamField>

  <ParamField path="id" type="string">
    Уникальный идентификатор сообщения (автоматически сгенерированный LangChain или возвращенный в ответе поставщика)
  </ParamField>

  <ParamField path="usage_metadata" type="dict | None">
    Метаданные использования сообщения, которые могут содержать счетчики токенов при наличии.
  </ParamField>

  <ParamField path="response_metadata" type="ResponseMetadata | None">
    Метаданные ответа сообщения.
  </ParamField>
</Accordion>

#### Вызовы инструментов

Когда модели совершают [вызовы инструментов](/oss/python/langchain/models#tool-calling), они включаются в [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage):

```python  theme={null}
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

def get_weather(location: str) -> str:
    """Получить погоду в местоположении."""
    ...

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("Какая погода в Париже?")

for tool_call in response.tool_calls:
    print(f"Инструмент: {tool_call['name']}")
    print(f"Аргументы: {tool_call['args']}")
    print(f"ID: {tool_call['id']}")
```

Другие структурированные данные, такие как рассуждения или цитаты, также могут появляться в [содержании](/oss/python/langchain/messages#содержание-сообщения) сообщения.

#### Использование токенов

[`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) может содержать счетчики токенов и другие метаданные использования в своем поле [`usage_metadata`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.UsageMetadata):

```python  theme={null}
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

response = model.invoke("Здравствуйте!")
response.usage_metadata
```

```
{'input_tokens': 8,
 'output_tokens': 304,
 'total_tokens': 312,
 'input_token_details': {'audio': 0, 'cache_read': 0},
 'output_token_details': {'audio': 0, 'reasoning': 256}}
```

Смотрите [`UsageMetadata`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.UsageMetadata) для получения подробной информации.

#### Потоковая передача и фрагменты

Во время потоковой передачи вы будете получать объекты [`AIMessageChunk`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessageChunk), которые можно объединить в полноценный объект сообщения:

```python  theme={null}
chunks = []
full_message = None
for chunk in model.stream("Привет"):
    chunks.append(chunk)
    print(chunk.text)
    full_message = chunk if full_message is None else full_message + chunk
```

<Note>
  Узнайте больше:

  * [Потоковая передача токенов из чат-моделей](/oss/python/langchain/models#stream)
  * [Потоковая передача токенов и/или шагов из агентов](/oss/python/langchain/streaming)
</Note>

***

### Сообщение инструмента

Для моделей, поддерживающих [вызовы инструментов](/oss/python/langchain/models#tool-calling), AI-сообщения могут содержать вызовы инструментов. Сообщения инструментов используются для передачи результатов выполнения одного инструмента обратно в модель.

[Инструменты](/oss/python/langchain/tools) могут генерировать объекты [`ToolMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.ToolMessage) напрямую. Ниже мы покажем простой пример. Подробнее читайте в [руководстве по инструментам](/oss/python/langchain/tools).

```python  theme={null}
from langchain.messages import AIMessage
from langchain.messages import ToolMessage

# После того, как модель совершает вызов инструмента
# (Здесь мы демонстрируем ручное создание сообщений для краткости)
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "Сан-Франциско"},
        "id": "call_123"
    }]
)

# Выполнить инструмент и создать сообщение результата
weather_result = "Солнечно, 72°F"
tool_message = ToolMessage(
    content=weather_result,
    tool_call_id="call_123"  # Должен совпадать с ID вызова
)

# Продолжить беседу
messages = [
    HumanMessage("Какая погода в Сан-Франциско?"),
    ai_message,  # Вызов инструмента модели
    tool_message,  # Результат выполнения инструмента
]
response = model.invoke(messages)  # Модель обрабатывает результат
```

<Accordion title="Атрибуты">
  <ParamField path="content" type="string" required>
    Строковое представление вывода вызова инструмента.
  </ParamField>

  <ParamField path="tool_call_id" type="string" required>
    ID вызова инструмента, на который отвечает это сообщение. Должен совпадать с ID вызова инструмента в [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage).
  </ParamField>

  <ParamField path="name" type="string" required>
    Имя вызванного инструмента.
  </ParamField>

  <ParamField path="artifact" type="dict">
    Дополнительные данные, не отправляемые в модель, но доступные для программного доступа.
  </ParamField>
</Accordion>

<Note>
  Поле `artifact` хранит дополнительные данные, которые не будут отправлены в модель, но могут быть доступны программно. Это полезно для хранения сырых результатов, отладочной информации или данных для последующей обработки без загромождения контекста модели.

  <Accordion title="Пример: Использование артефакта для метаданных поиска">
    Например, [поисковый](/oss/python/langchain/retrieval) инструмент может извлечь отрывок из документа для ссылки моделью. Где содержание сообщения `content` содержит текст, на который будет ссылаться модель, `artifact` может содержать идентификаторы документов или другие метаданные, которые приложение может использовать (например, для отображения страницы). Смотрите пример ниже:

    ```python  theme={null}
    from langchain.messages import ToolMessage

    # Отправляется в модель
    message_content = "Это было лучшее из времен, это было худшее из времен."

    # Артефакт доступен вниз по потоку
    artifact = {"document_id": "doc_123", "page": 0}

    tool_message = ToolMessage(
        content=message_content,
        tool_call_id="call_123",
        name="search_books",
        artifact=artifact,
    )
    ```

    Смотрите [учебник RAG](/oss/python/langchain/rag) для комплексного примера создания [агентов](/oss/python/langchain/agents) с извлечением с помощью LangChain.
  </Accordion>
</Note>

***

## Содержание сообщения

Вы можете думать о содержании сообщения как о полезной нагрузке данных, которая отправляется в модель. Сообщения имеют атрибут `content`, который слабо типизирован, поддерживающий строки и списки нетипизированных объектов (например, словарей). Это позволяет поддерживать родные структуры поставщиков непосредственно в чат-моделях LangChain, такие как [мультимодальное](#мультимодальное) содержание и другие данные.

Отдельно, LangChain предоставляет выделенные типы содержания для текста, рассуждений, цитат, мультимодальных данных, серверных вызовов инструментов и другого содержания сообщений. Смотрите [блоки содержания](#стандартные-блоки-содержания) ниже.

Чат-модели LangChain принимают содержание сообщений в атрибуте `content`.

Это может содержать либо:

1. Строку
2. Список блоков содержания в родном формате поставщика
3. Список [стандартных блоков содержания LangChain](#стандартные-блоки-содержания)

Смотрите ниже пример использования [мультимодальных](#мультимодальное) входных данных:

```python  theme={null}
from langchain.messages import HumanMessage

# Строковое содержание
human_message = HumanMessage("Здравствуйте, как вы?")

# Родной формат поставщика (например, OpenAI)
human_message = HumanMessage(content=[
    {"type": "text", "text": "Здравствуйте, как вы?"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])

# Список стандартных блоков содержания
human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "Здравствуйте, как вы?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])
```

<Tip>
  Указание `content_blocks` при инициализации сообщения все равно заполнит сообщение
  `content`, но обеспечивает безопасный интерфейс для этого.
</Tip>

### Стандартные блоки содержания

LangChain предоставляет стандартное представление для содержания сообщений, которое работает со всеми поставщиками.

Объекты сообщений реализуют свойство `content_blocks`, которое лениво анализирует атрибут `content` в стандартное, безопасное по типам представление. Например, сообщения, сгенерированные из [`ChatAnthropic`](/oss/python/integrations/chat/anthropic) или [`ChatOpenAI`](/oss/python/integrations/chat/openai), будут включать блоки `thinking` или `reasoning` в формате соответствующего поставщика, но могут быть лениво проанализированы в согласованное представление [`ReasoningContentBlock`](#справочник-по-блокам-содержания):

<Tabs>
  <Tab title="Anthropic">
    ```python  theme={null}
    from langchain.messages import AIMessage

    message = AIMessage(
        content=[
            {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."},
            {"type": "text", "text": "..."},
        ],
        response_metadata={"model_provider": "anthropic"}
    )
    message.content_blocks
    ```

    ```
    [{'type': 'reasoning',
      'reasoning': '...',
      'extras': {'signature': 'WaUjzkyp...'}},
     {'type': 'text', 'text': '...'}]
    ```
  </Tab>

  <Tab title="OpenAI">
    ```python  theme={null}
    from langchain.messages import AIMessage

    message = AIMessage(
        content=[
            {
                "type": "reasoning",
                "id": "rs_abc123",
                "summary": [
                    {"type": "summary_text", "text": "резюме 1"},
                    {"type": "summary_text", "text": "резюме 2"},
                ],
            },
            {"type": "text", "text": "...", "id": "msg_abc123"},
        ],
        response_metadata={"model_provider": "openai"}
    )
    message.content_blocks
    ```

    ```
    [{'type': 'reasoning', 'id': 'rs_abc123', 'reasoning': 'резюме 1'},
     {'type': 'reasoning', 'id': 'rs_abc123', 'reasoning': 'резюме 2'},
     {'type': 'text', 'text': '...', 'id': 'msg_abc123'}]
    ```
  </Tab>
</Tabs>

Смотрите [руководства по интеграции](/oss/python/integrations/providers/overview), чтобы начать работу с
поставщиком вывода по вашему выбору.

<Note>
  **Сериализация стандартного содержания**

  Если приложению вне LangChain нужен доступ к стандартному представлению блока содержания,
  вы можете согласиться на хранение блоков содержания в содержании сообщения.

  Для этого вы можете установить переменную окружения `LC_OUTPUT_VERSION` в значение `v1`. Или,
  инициализировать любую чат-модель с `output_version="v1"`:

  ```python  theme={null}
  from langchain.chat_models import init_chat_model

  model = init_chat_model("gpt-5-nano", output_version="v1")
  ```
</Note>

### Мультимодальное

**Мультимодальность** относится к способности работать с данными, которые приходят в разных
формах, таких как текст, аудио, изображения и видео. LangChain включает стандартные типы
для этих данных, которые можно использовать со всеми поставщиками.

[Чат-модели](/oss/python/langchain/models) могут принимать мультимодальные данные в качестве входных и генерировать
их в качестве выходных. Ниже мы показываем короткие примеры входных сообщений с мультимодальными данными.

<Note>
  Дополнительные ключи могут быть включены на верхнем уровне в блоке содержания или вложены в `"extras": {"key": value}`.

  [OpenAI](/oss/python/integrations/chat/openai#pdfs) и [AWS Bedrock Converse](/oss/python/integrations/chat/bedrock),
  например, требуют имя файла для PDF. Смотрите [страницу поставщика](/oss/python/integrations/providers/overview)
  для выбранной вами модели для получения подробной информации.
</Note>

<CodeGroup>
  ```python Ввод изображения theme={null}
  # Из URL
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого изображения."},
          {"type": "image", "url": "https://example.com/path/to/image.jpg"},
      ]
  }

  # Из данных base64
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого изображения."},
          {
              "type": "image",
              "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
              "mime_type": "image/jpeg",
          },
      ]
  }

  # Из управляемого поставщиком ID файла
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого изображения."},
          {"type": "image", "file_id": "file-abc123"},
      ]
  }
  ```

  ```python Ввод PDF-документа theme={null}
  # Из URL
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого документа."},
          {"type": "file", "url": "https://example.com/path/to/document.pdf"},
      ]
  }

  # Из данных base64
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого документа."},
          {
              "type": "file",
              "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
              "mime_type": "application/pdf",
          },
      ]
  }

  # Из управляемого поставщиком ID файла
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого документа."},
          {"type": "file", "file_id": "file-abc123"},
      ]
  }
  ```

  ```python Ввод аудио theme={null}
  # Из данных base64
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого аудио."},
          {
              "type": "audio",
              "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
              "mime_type": "audio/wav",
          },
      ]
  }

  # Из управляемого поставщиком ID файла
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого аудио."},
          {"type": "audio", "file_id": "file-abc123"},
      ]
  }
  ```

  ```python Ввод видео theme={null}
  # Из данных base64
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого видео."},
          {
              "type": "video",
              "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
              "mime_type": "video/mp4",
          },
      ]
  }

  # Из управляемого поставщиком ID файла
  message = {
      "role": "user",
      "content": [
          {"type": "text", "text": "Опишите содержание этого видео."},
          {"type": "video", "file_id": "file-abc123"},
      ]
  }
  ```
</CodeGroup>

<Warning>
  Не все модели поддерживают все типы файлов. Проверьте [справку](https://reference.langchain.com/python/integrations/) поставщика модели на предмет поддерживаемых форматов и ограничений по размеру.
</Warning>

### Справочник по блокам содержания

Блоки содержания представлены (либо при создании сообщения, либо при доступе к свойству `content_blocks`) как список типизированных словарей. Каждый элемент в списке должен соответствовать одному из следующих типов блоков:

<AccordionGroup>
  <Accordion title="Основные" icon="cube">
    <AccordionGroup>
      <Accordion title="TextContentBlock" icon="text">
        **Назначение:** Стандартный текстовый вывод

        <ParamField body="type" type="string" required>
          Всегда `"text"`
        </ParamField>

        <ParamField body="text" type="string" required>
          Текстовое содержание
        </ParamField>

        <ParamField body="annotations" type="object[]">
          Список аннотаций для текста
        </ParamField>

        <ParamField body="extras" type="object">
          Дополнительные данные, специфичные для поставщика
        </ParamField>

        **Пример:**

        ```python  theme={null}
        {
            "type": "text",
            "text": "Привет, мир",
            "annotations": []
        }
        ```
      </Accordion>

      <Accordion title="ReasoningContentBlock" icon="brain">
        **Назначение:** Шаги рассуждений модели

        <ParamField body="type" type="string" required>
          Всегда `"reasoning"`
        </ParamField>

        <ParamField body="reasoning" type="string">
          Содержание рассуждений
        </ParamField>

        <ParamField body="extras" type="object">
          Дополнительные данные, специфичные для поставщика
        </ParamField>

        **Пример:**

        ```python  theme={null}
        {
            "type": "reasoning",
            "reasoning": "Пользователь спрашивает о...",
            "extras": {"signature": "abc123"},
        }
        ```
      </Accordion>
    </AccordionGroup>
  </Accordion>

  <Accordion title="Мультимодальные" icon="images">
    <AccordionGroup>
      <Accordion title="ImageContentBlock" icon="image">
        **Назначение:** Данные изображения

        <ParamField body="type" type="string" required>
          Всегда `"image"`
        </ParamField>

        <ParamField body="url" type="string">
          URL, указывающий на расположение изображения.
        </ParamField>

        <ParamField body="base64" type="string">
          Данные изображения в кодировке Base64.
        </ParamField>

        <ParamField body="id" type="string">
          Ссылочный ID на внешнее хранилище изображения (например, в файловой системе поставщика или в бакете).
        </ParamField>

        <ParamField body="mime_type" type="string">
          [MIME-тип](https://www.iana.org/assignments/media-types/media-types.xhtml#image) изображения (например, `image/jpeg`, `image/png`)
        </ParamField>
      </Accordion>

      <Accordion title="AudioContentBlock" icon="volume-high">
        **Назначение:** Данные аудио

        <ParamField body="type" type="string" required>
          Всегда `"audio"`
        </ParamField>

        <ParamField body="url" type="string">
          URL, указывающий на расположение аудио.
        </ParamField>

        <ParamField body="base64" type="string">
          Данные аудио в кодировке Base64.
        </ParamField>

        <ParamField body="id" type="string">
          Ссылочный ID на внешний аудиофайл (например, в файловой системе поставщика или в бакете).
        </ParamField>

        <ParamField body="mime_type" type="string">
          [MIME-тип](https://www.iana.org/assignments/media-types/media-types.xhtml#audio) аудио (например, `audio/mpeg`, `audio/wav`)
        </ParamField>
      </Accordion>

      <Accordion title="VideoContentBlock" icon="video">
        **Назначение:** Данные видео

        <ParamField body="type" type="string" required>
          Всегда `"video"`
        </ParamField>

        <ParamField body="url" type="string">
          URL, указывающий на расположение видео.
        </ParamField>

        <ParamField body="base64" type="string">
          Данные видео в кодировке Base64.
        </ParamField>

        <ParamField body="id" type="string">
          Ссылочный ID на внешний видеофайл (например, в файловой системе поставщика или в бакете).
        </ParamField>

        <ParamField body="mime_type" type="string">
          [MIME-тип](https://www.iana.org/assignments/media-types/media-types.xhtml#video) видео (например, `video/mp4`, `video/webm`)
        </ParamField>
      </Accordion>

      <Accordion title="FileContentBlock" icon="file">
        **Назначение:** Общие файлы (PDF и т.д.)

        <ParamField body="type" type="string" required>
          Всегда `"file"`
        </ParamField>

        <ParamField body="url" type="string">
          URL, указывающий на расположение файла.
        </ParamField>

        <ParamField body="base64" type="string">
          Данные файла в кодировке Base64.
        </ParamField>

        <ParamField body="id" type="string">
          Ссылочный ID на внешний файл (например, в файловой системе поставщика или в бакете).
        </ParamField>

        <ParamField body="mime_type" type="string">
          [MIME-тип](https://www.iana.org/assignments/media-types/media-types.xhtml) файла (например, `application/pdf`)
        </ParamField>
      </Accordion>

      <Accordion title="PlainTextContentBlock" icon="align-left">
        **Назначение:** Текст документов (`.txt`, `.md`)

        <ParamField body="type" type="string" required>
          Всегда `"text-plain"`
        </ParamField>

        <ParamField body="text" type="string">
          Текстовое содержание
        </ParamField>

        <ParamField body="mime_type" type="string">
          [MIME-тип](https://www.iana.org/assignments/media-types/media-types.xhtml) текста (например, `text/plain`, `text/markdown`)
        </ParamField>
      </Accordion>
    </AccordionGroup>
  </Accordion>

  <Accordion title="Вызовы инструментов" icon="wrench">
    <AccordionGroup>
      <Accordion title="ToolCall" icon="function">
        **Назначение:** Вызовы функций

        <ParamField body="type" type="string" required>
          Всегда `"tool_call"`
        </ParamField>

        <ParamField body="name" type="string" required>
          Имя вызываемого инструмента
        </ParamField>

        <ParamField body="args" type="object" required>
          Аргументы для передачи инструменту
        </ParamField>

        <ParamField body="id" type="string" required>
          Уникальный идентификатор для этого вызова инструмента
        </ParamField>

        **Пример:**

        ```python  theme={null}
        {
            "type": "tool_call",
            "name": "search",
            "args": {"query": "погода"},
            "id": "call_123"
        }
        ```
      </Accordion>

      <Accordion title="ToolCallChunk" icon="puzzle-piece">
        **Назначение:** Фрагменты вызовов инструментов при потоковой передаче

        <ParamField body="type" type="string" required>
          Всегда `"tool_call_chunk"`
        </ParamField>

        <ParamField body="name" type="string">
          Имя вызываемого инструмента
        </ParamField>

        <ParamField body="args" type="string">
          Частичные аргументы инструмента (может быть неполным JSON)
        </ParamField>

        <ParamField body="id" type="string">
          Идентификатор вызова инструмента
        </ParamField>

        <ParamField body="index" type="number | string">
          Позиция этого фрагмента в потоке
        </ParamField>
      </Accordion>

      <Accordion title="InvalidToolCall" icon="triangle-exclamation">
        **Назначение:** Неправильные вызовы, предназначенные для отлова ошибок парсинга JSON.

        <ParamField body="type" type="string" required>
          Всегда `"invalid_tool_call"`
        </ParamField>

        <ParamField body="name" type="string">
          Имя инструмента, который не удалось вызвать
        </ParamField>

        <ParamField body="args" type="object">
          Аргументы для передачи инструменту
        </ParamField>

        <ParamField body="error" type="string">
          Описание того, что пошло не так
        </ParamField>
      </Accordion>
    </AccordionGroup>
  </Accordion>

  <Accordion title="Серверное выполнение инструментов" icon="server">
    <AccordionGroup>
      <Accordion title="ServerToolCall" icon="wrench">
        **Назначение:** Вызов инструмента, выполняемый на стороне сервера.

        <ParamField body="type" type="string" required>
          Всегда `"server_tool_call"`
        </ParamField>

        <ParamField body="id" type="string" required>
          Идентификатор, связанный с вызовом инструмента.
        </ParamField>

        <ParamField body="name" type="string" required>
          Имя вызываемого инструмента.
        </ParamField>

        <ParamField body="args" type="string" required>
          Частичные аргументы инструмента (может быть неполным JSON)
        </ParamField>
      </Accordion>

      <Accordion title="ServerToolCallChunk" icon="puzzle-piece">
        **Назначение:** Фрагменты вызовов инструментов на стороне сервера при потоковой передаче

        <ParamField body="type" type="string" required>
          Всегда `"server_tool_call_chunk"`
        </ParamField>

        <ParamField body="id" type="string">
          Идентификатор, связанный с вызовом инструмента.
        </ParamField>

        <ParamField body="name" type="string">
          Имя вызываемого инструмента
        </ParamField>

        <ParamField body="args" type="string">
          Частичные аргументы инструмента (может быть неполным JSON)
        </ParamField>

        <ParamField body="index" type="number | string">
          Позиция этого фрагмента в потоке
        </ParamField>
      </Accordion>

      <Accordion title="ServerToolResult" icon="box-open">
        **Назначение:** Результаты поиска

        <ParamField body="type" type="string" required>
          Всегда `"server_tool_result"`
        </ParamField>

        <ParamField body="tool_call_id" type="string" required>
          Идентификатор соответствующего вызова серверного инструмента.
        </ParamField>

        <ParamField body="id" type="string">
          Идентификатор, связанный с результатом серверного инструмента.
        </ParamField>

        <ParamField body="status" type="string" required>
          Статус выполнения инструмента на стороне сервера. `"success"` или `"error"`.
        </ParamField>

        <ParamField body="output">
          Вывод выполненного инструмента.
        </ParamField>
      </Accordion>
    </AccordionGroup>
  </Accordion>

  <Accordion title="Блоки, специфичные для поставщика" icon="plug">
    <Accordion title="NonStandardContentBlock" icon="asterisk">
      **Назначение:** Аварийный люк для поставщика

      <ParamField body="type" type="string" required>
        Всегда `"non_standard"`
      </ParamField>

      <ParamField body="value" type="object" required>
        Структура данных, специфичная для поставщика
      </ParamField>

      **Использование:** Для экспериментальных или уникальных функций поставщика
    </Accordion>

    Дополнительные типы содержания, специфичные для поставщика, могут быть найдены в [справочной документации](/oss/python/integrations/providers/overview) каждого поставщика моделей.
  </Accordion>
</AccordionGroup>

<Tip>
  Просмотрите канонические определения типов в [справке API](https://reference.langchain.com/python/langchain/messages).
</Tip>

<Info>
  Блоки содержания были представлены как новое свойство сообщений в LangChain v1 для стандартизации форматов содержания между поставщиками при сохранении обратной совместимости с существующим кодом.

  Блоки содержания не являются заменой свойства [`content`](https://reference.langchain.com/python/langchain_core/language_models/#langchain_core.messages.BaseMessage.content), а скорее новым свойством, которое можно использовать для доступа к содержанию сообщения в стандартизированном формате.
</Info>

## Использование с чат-моделями

[Чат-модели](/oss/python/langchain/models) принимают последовательность объектов сообщений в качестве входных данных и возвращают [`AIMessage`](https://reference.langchain.com/python/langchain/messages/#langchain.messages.AIMessage) в качестве выходных данных. Взаимодействия часто не имеют состояния, поэтому простой диалоговый цикл включает вызов модели со списком сообщений, который постоянно растет.

Обратитесь к приведенным ниже руководствам, чтобы узнать больше:

* Встроенные функции для [сохранения и управления историями бесед](/oss/python/langchain/short-term-memory)
* Стратегии управления окнами контекста, включая [обрезку и суммирование сообщений](/oss/python/langchain/short-term-memory#common-patterns)

***
<Callout icon="pen-to-square" iconType="regular">
  [Редактировать источник этой страницы на GitHub.](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/messages.mdx)
</Callout>

<Tip icon="terminal" iconType="regular">
  [Подключите эти документы программно](/use-these-docs) к Claude, VSCode и другим через MCP для получения ответов в реальном времени.
</Tip>

---
> Чтобы найти навигацию и другие страницы в этой документации, загрузите файл llms.txt по адресу: https://docs.langchain.com/llms.txt