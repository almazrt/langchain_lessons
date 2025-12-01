# Урок 6: Специализированные применения LangChain

## Введение

В предыдущих уроках мы рассмотрели основы работы с LangChain, начиная с простых цепочек и заканчивая продвинутыми техниками и лучшими практиками. В этом уроке мы погрузимся в специализированные применения LangChain для решения конкретных бизнес-задач и реальных сценариев использования.

## Чат-боты для бизнеса

Чат-боты стали неотъемлемой частью современного бизнеса. LangChain предоставляет мощные инструменты для создания интеллектуальных чат-ботов.

### Чат-бот с контекстом компании

```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# Загрузка документов компании
loader = TextLoader("company_docs.txt")
documents = loader.load()

# Разделение документов на части
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# Создание векторного хранилища
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)

# Инициализация модели
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")

# Создание памяти
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Создание цепочки
qa = ConversationalRetrievalChain.from_llm(
    llm,
    vectorstore.as_retriever(),
    memory=memory
)

# Использование
query = "Какие услуги предлагает ваша компания?"
result = qa({"question": query})
print(result["answer"])
```

### Чат-бот с несколькими языками

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Шаблон для многоязычного чат-бота
template = """
Вы - многоязычный ассистент. Отвечайте на языке пользователя.
Если пользователь пишет на русском, отвечайте на русском.
Если пользователь пишет на английском, отвечайте на английском.

История чата:
{history}

Пользователь: {input}
Ассистент:
"""

prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
chain = prompt | llm | StrOutputParser()

# Пример использования
history = "Пользователь: Привет\nАссистент: Здравствуйте! Чем могу помочь?"
response = chain.invoke({"history": history, "input": "Как дела?"})
print(response)
```

## Генерация контента

LangChain может быть использован для автоматической генерации различных типов контента.

### Генератор маркетинговых текстов

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Шаблон для генерации рекламных текстов
ad_template = """
Создайте привлекательный рекламный текст для продукта "{product}".
Целевая аудитория: {audience}
Основные преимущества: {benefits}
Стиль: {style}

Рекламный текст:
"""

ad_prompt = PromptTemplate.from_template(ad_template)
llm = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0.7)
ad_chain = ad_prompt | llm | StrOutputParser()

# Генерация рекламного текста
result = ad_chain.invoke({
    "product": "умный термос",
    "audience": "молодые профессионалы",
    "benefits": "сохраняет температуру до 24 часов, стильный дизайн, экологичен",
    "style": "современный, энергичный"
})
print(result)
```

### Генератор отчетов

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Шаблон для генерации отчетов
report_template = """
Проанализируйте следующие данные и создайте профессиональный отчет:

Данные:
{data}

Требования к отчету:
- Формат: {format}
- Длина: {length}
- Акцент на: {focus}

Отчет:
"""

report_prompt = PromptTemplate.from_template(report_template)
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
report_chain = report_prompt | llm | StrOutputParser()

# Генерация отчета
sales_data = """
Январь: 100 единиц, доход $10,000
Февраль: 120 единиц, доход $12,000
Март: 150 единиц, доход $15,000
"""
result = report_chain.invoke({
    "data": sales_data,
    "format": "таблица с анализом",
    "length": "1 абзац",
    "focus": "тенденции роста"
})
print(result)
```

## Анализ данных и документов

LangChain может помочь в анализе больших объемов данных и документов.

### Анализ отзывов клиентов

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Модель для структурированного анализа отзывов
class ReviewAnalysis(BaseModel):
    sentiment: str = Field(description="Общее настроение отзыва: положительное, отрицательное или нейтральное")
    key_points: List[str] = Field(description="Ключевые моменты из отзыва")
    suggestions: List[str] = Field(description="Предложения по улучшению")

# Шаблон для анализа отзывов
review_template = """
Проанализируйте следующий отзыв клиента и предоставьте структурированный ответ:

Отзыв: {review}

{format_instructions}
"""

parser = JsonOutputParser(pydantic_object=ReviewAnalysis)
review_prompt = PromptTemplate(
    template=review_template,
    input_variables=["review"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
review_chain = review_prompt | llm | parser

# Анализ отзыва
review = "Заказ пришел быстро, но качество товара оставляет желать лучшего. Упаковка была повреждена."
result = review_chain.invoke({"review": review})
print(result)
```

### Юридический анализ документов

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Шаблон для юридического анализа
legal_template = """
Вы - юридический эксперт. Проанализируйте следующий документ и выделите важные юридические аспекты:

Документ:
{document}

Проанализируйте:
1. Правовые обязательства сторон
2. Возможные риски
3. Рекомендации по улучшению

Анализ:
"""

legal_prompt = PromptTemplate.from_template(legal_template)
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
legal_chain = legal_prompt | llm | StrOutputParser()

# Анализ договора (пример)
contract = """
ДОГОВОР ПОСТАВКИ
1. Поставщик обязуется передать Покупателю товар в течение 30 дней.
2. Покупатель обязан оплатить товар в течение 10 дней после получения.
3. В случае просрочки поставщик вправе потребовать пеню в размере 0.1% от стоимости товара за каждый день просрочки.
"""
result = legal_chain.invoke({"document": contract})
print(result)
```

## Интеграция с внешними системами

LangChain легко интегрируется с различными внешними системами и API.

### Интеграция с CRM системой

```python
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import json

# Имитация CRM API
class CRMAPI:
    def __init__(self):
        self.customers = {
            "1": {"name": "Иван Петров", "email": "ivan@example.com", "status": "VIP"},
            "2": {"name": "Мария Сидорова", "email": "maria@example.com", "status": "Regular"}
        }
    
    def get_customer_info(self, customer_id):
        return self.customers.get(customer_id, "Клиент не найден")
    
    def update_customer_status(self, customer_id, status):
        if customer_id in self.customers:
            self.customers[customer_id]["status"] = status
            return f"Статус клиента {customer_id} обновлен на {status}"
        return "Клиент не найден"

# Инициализация CRM API
crm = CRMAPI()

# Создание инструментов для агента
tools = [
    Tool(
        name="GetCustomerInfo",
        func=lambda customer_id: crm.get_customer_info(customer_id),
        description="Получает информацию о клиенте по ID"
    ),
    Tool(
        name="UpdateCustomerStatus",
        func=lambda x: crm.update_customer_status(*x.split(",")),
        description="Обновляет статус клиента. Формат: customer_id,status"
    )
]

# Создание агента
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
prompt = PromptTemplate.from_template("""
Ответь на вопрос пользователя, используя доступные инструменты.

Вопрос: {input}
{agent_scratchpad}
""")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Использование агента
result = agent_executor.invoke({"input": "Покажи информацию о клиенте с ID 1"})
print(result["output"])
```

### Интеграция с системами электронной коммерции

```python
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# Имитация eCommerce API
class ECommerceAPI:
    def __init__(self):
        self.products = {
            "1": {"name": "Смартфон", "price": 500, "stock": 10},
            "2": {"name": "Ноутбук", "price": 1000, "stock": 5}
        }
    
    def get_product_info(self, product_id):
        return self.products.get(product_id, "Товар не найден")
    
    def check_inventory(self, product_id):
        product = self.products.get(product_id)
        if product:
            return f"Остаток товара {product['name']}: {product['stock']} шт."
        return "Товар не найден"
    
    def process_order(self, product_id, quantity):
        product = self.products.get(product_id)
        if not product:
            return "Товар не найден"
        
        if product["stock"] >= int(quantity):
            product["stock"] -= int(quantity)
            total = int(quantity) * product["price"]
            return f"Заказ оформлен. Общая стоимость: ${total}. Остаток: {product['stock']} шт."
        else:
            return f"Недостаточно товара на складе. Доступно: {product['stock']} шт."

# Инициализация eCommerce API
ecommerce = ECommerceAPI()

# Создание инструментов
tools = [
    Tool(
        name="GetProductInfo",
        func=lambda product_id: ecommerce.get_product_info(product_id),
        description="Получает информацию о товаре по ID"
    ),
    Tool(
        name="CheckInventory",
        func=lambda product_id: ecommerce.check_inventory(product_id),
        description="Проверяет наличие товара на складе"
    ),
    Tool(
        name="ProcessOrder",
        func=lambda x: ecommerce.process_order(*x.split(",")),
        description="Оформляет заказ. Формат: product_id,quantity"
    )
]

# Создание агента
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
prompt = PromptTemplate.from_template("""
Ты помощник по электронной коммерции. Помоги пользователю с покупками.

Вопрос: {input}
{agent_scratchpad}
""")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Использование агента
result = agent_executor.invoke({"input": "Проверь наличие смартфона и оформи заказ на 2 штуки"})
print(result["output"])
```

## Образовательные приложения

LangChain может быть использован для создания образовательных приложений и систем обучения.

### Интерактивный учебник

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Шаблон для создания учебного материала
tutorial_template = """
Создай обучающий материал по теме "{topic}" для уровня "{level}".

Требования:
- Формат: {format}
- Длина: {length}
- Включить примеры: {examples}
- Стиль: {style}

Учебный материал:
"""

tutorial_prompt = PromptTemplate.from_template(tutorial_template)
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
tutorial_chain = tutorial_prompt | llm | StrOutputParser()

# Генерация учебного материала
result = tutorial_chain.invoke({
    "topic": "основы Python",
    "level": "начинающий",
    "format": "пошаговое руководство",
    "length": "3 абзаца",
    "examples": "да",
    "style": "дружелюбный, понятный"
})
print(result)
```

### Система проверки знаний

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Модель для вопросов
class Question(BaseModel):
    question: str = Field(description="Вопрос")
    options: List[str] = Field(description="Варианты ответов")
    correct_answer: str = Field(description="Правильный ответ")

# Модель для теста
class Quiz(BaseModel):
    questions: List[Question] = Field(description="Список вопросов")

# Шаблон для генерации теста
quiz_template = """
Создай тест из {num_questions} вопросов по теме "{topic}" для уровня "{level}".

{format_instructions}
"""

parser = JsonOutputParser(pydantic_object=Quiz)
quiz_prompt = PromptTemplate(
    template=quiz_template,
    input_variables=["num_questions", "topic", "level"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
quiz_chain = quiz_prompt | llm | parser

# Генерация теста
result = quiz_chain.invoke({
    "num_questions": "3",
    "topic": "машинное обучение",
    "level": "начинающий"
})
print(result)
```

## Практическое задание

1. Создайте чат-бота для компании, который может отвечать на вопросы о продуктах и услугах, используя документы компании
2. Разработайте систему генерации маркетингового контента для нескольких каналов (социальные сети, email, сайт)
3. Создайте инструмент для анализа отзывов клиентов и автоматической классификации по категориям
4. Реализуйте интеграцию с внешней системой (например, CRM или eCommerce платформой) через агента
5. Разработайте образовательное приложение с возможностью генерации персонализированных учебных материалов

## Советы и лучшие практики

1. **Адаптируйте решения под конкретные бизнес-задачи** - не пытайтесь применить универсальное решение ко всем случаям
2. **Интегрируйтесь с существующими системами** - используйте уже имеющиеся данные и процессы
3. **Обеспечьте безопасность данных** - при работе с конфиденциальной информацией используйте соответствующие меры защиты
4. **Тестируйте на реальных данных** - проверяйте решения на данных, близких к production
5. **Обеспечьте масштабируемость** - проектируйте решения с учетом будущего роста нагрузки
6. **Мониторьте эффективность** - внедряйте системы отслеживания метрик и показателей эффективности
7. **Обеспечьте отказоустойчивость** - планируйте обработку ошибок и сбоев в интеграциях

## Заключение

В этом уроке мы рассмотрели специализированные применения LangChain для решения конкретных бизнес-задач. Мы изучили создание чат-ботов для бизнеса, генерацию контента, анализ данных и документов, интеграцию с внешними системами и образовательные приложения.

Эти примеры демонстрируют, как LangChain может быть применен в различных сферах для автоматизации процессов, повышения эффективности и создания интеллектуальных решений. Помните, что ключ к успешному внедрению - это глубокое понимание бизнес-процессов и потребностей пользователей.

В следующем уроке мы рассмотрим будущее развития LangChain и новые возможности, которые появятся в следующих версиях фреймворка.