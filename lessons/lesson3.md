# Урок 3: Работа с внешними данными и индексами в LangChain

## Введение

В предыдущих уроках мы познакомились с основами LangChain, работой с памятью и созданием сложных цепочек. В этом уроке мы рассмотрим работу с внешними данными и индексами, что является ключевым аспектом при создании приложений, способных анализировать большие объемы информации.

## Работа с документами

В LangChain документы представлены классом [Document](file:///home/user1/langchain/.venv/lib/python3.11/site-packages/langchain_core/documents/base.py#L35-L111), который содержит текстовое содержимое и метаданные.

### Создание документов

```python
from langchain_core.documents import Document

# Создание простого документа
doc = Document(page_content="Это пример содержимого документа")

# Создание документа с метаданными
doc_with_metadata = Document(
    page_content="Это документ с метаданными",
    metadata={"source": "manual", "page": 1}
)
```

## Загрузчики документов

Загрузчики документов (Loaders) позволяют загружать данные из различных источников: файлов, веб-страниц, баз данных и т.д.

### Загрузка из текстового файла

```python
from langchain_community.document_loaders import TextLoader

# Загрузка текстового файла
loader = TextLoader("data/document.txt")
documents = loader.load()
```

### Загрузка из PDF

```python
from langchain_community.document_loaders import PyPDFLoader

# Загрузка PDF файла
loader = PyPDFLoader("data/document.pdf")
pages = loader.load_and_split()
```

## Разделители текста (Text Splitters)

При работе с большими документами их необходимо разбивать на части для эффективной обработки.

### RecursiveCharacterTextSplitter

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Создание разделителя
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

# Разделение документов
texts = text_splitter.split_documents(documents)
```

## Векторные хранилища

Векторные хранилища позволяют эффективно хранить и искать векторные представления текстов.

### Создание векторного хранилища с Chroma

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Инициализация эмбеддингов
embeddings = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)

# Создание векторного хранилища
vectorstore = Chroma.from_documents(
    documents=texts,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

## Полный пример работы с внешними данными

```
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Проверяем наличие API ключа
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в переменных окружения или файле .env")
            return
        
        # Создаем пример документа
        sample_document = Document(
            page_content="""
            Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием 
            программного обеспечения и алгоритмов, наделяющих компьютеры способностью к обучению, 
            рассуждению и принятию решений. Современные достижения в области ИИ позволили создать 
            мощные языковые модели, способные понимать и генерировать человеческий язык.
            
            Одним из ключевых направлений ИИ является машинное обучение, которое позволяет системам 
            автоматически улучшать свою производительность на основе опыта. Глубокое обучение, 
            подмножество машинного обучения, использует нейронные сети для решения сложных задач.
            
            Большие языковые модели, такие как GPT, используют глубокое обучение для обработки 
            естественного языка. Они обучены на огромных объемах текстовых данных и могут 
            выполнять различные задачи: от ответов на вопросы до написания текстов.
            """,
            metadata={"source": "ai_introduction", "topic": "artificial intelligence"}
        )
        
        # Разделение документа на части
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50,
            length_function=len,
        )
        
        texts = text_splitter.split_documents([sample_document])
        print(f"Документ разделен на {len(texts)} частей")
        
        # Инициализируем модель через OpenRouter
        llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Инициализация эмбеддингов
        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Создание векторного хранилища
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=embeddings,
            persist_directory="./chroma_db"
        )
        
        # Поиск похожих документов
        query = "Что такое машинное обучение?"
        similar_docs = vectorstore.similarity_search(query, k=2)
        
        print(f"\nПоиск по запросу: {query}")
        for i, doc in enumerate(similar_docs):
            print(f"\n--- Результат {i+1} ---")
            print(f"Содержимое: {doc.page_content}")
            print(f"Метаданные: {doc.metadata}")
        
        # Удаление временной базы данных
        import shutil
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()
```

## Цепочки с доступом к внешним данным

LangChain позволяет создавать цепочки, которые могут использовать внешние данные для генерации ответов.

### Retrieval Chain

```python
from langchain.chains import RetrievalQA
# Note: Depending on your LangChain version, the import path may vary

# Создание цепочки для поиска и ответов
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

# Использование цепочки
query = "Объясни концепцию больших языковых моделей"
result = qa_chain.invoke({"query": query})
print(result["result"])
```

## Практическое задание

1. Создайте приложение, которое загружает текстовый документ, разбивает его на части и сохраняет в векторном хранилище
2. Реализуйте поиск похожих документов по пользовательским запросам
3. Создайте цепочку, которая использует внешние данные для генерации ответов на вопросы
4. Добавьте метаданные к документам и реализуйте фильтрацию по ним

## Советы и лучшие практики

1. Выбирайте подходящий размер фрагментов при разделении документов (chunk_size)
2. Используйте перекрытие (chunk_overlap) для сохранения контекста между фрагментами
3. Храните векторные базы данных на диске для повторного использования
4. Используйте метаданные для организации и фильтрации документов
5. Очищайте временные файлы и базы данных после завершения работы

## Примечание о совместимости

Важно отметить, что при работе с LangChain могут возникнуть проблемы совместимости с другими библиотеками. Например, в нашем примере мы столкнулись с проблемой совместимости с NumPy 2.0, где функция `np.float_` была удалена. В таких случаях рекомендуется:

1. Проверять версии зависимостей в requirements.txt
2. Использовать виртуальные окружения для изоляции зависимостей
3. Следить за обновлениями документации LangChain

## Заключение

В этом уроке мы рассмотрели работу с внешними данными и индексами в LangChain. Мы научились загружать документы, разбивать их на части, создавать векторные представления и выполнять поиск похожих документов. Эти навыки являются основой для создания мощных приложений, способных работать с большими объемами информации. В следующем уроке мы изучим работу с агентами и автономными системами.