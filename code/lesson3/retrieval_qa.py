import os
import shutil
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
# Note: RetrievalQA import may need to be adjusted based on your LangChain version

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Проверяем наличие API ключа
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в переменных окружения или файле .env")
            return
        
        # Создаем пример документа с информацией о программировании
        programming_doc = Document(
            page_content="""
            Python - это высокоуровневый язык программирования общего назначения с широкой популярностью 
            благодаря своей простоте и читаемости. Он поддерживает несколько парадигм программирования, 
            включая объектно-ориентированное, функциональное и процедурное программирование.
            
            Основные преимущества Python включают:
            1. Простоту изучения и использования
            2. Богатую экосистему библиотек и фреймворков
            3. Кроссплатформенную совместимость
            4. Поддержку различных стилей программирования
            
            Python широко используется в веб-разработке, науке о данных, искусственном интеллекте, 
            автоматизации и многих других областях. Популярные фреймворки включают Django и Flask 
            для веб-разработки, NumPy и Pandas для анализа данных, TensorFlow и PyTorch для машинного обучения.
            
            Синтаксис Python делает код легко читаемым и понятным. Например, для создания списка 
            квадратов чисел можно использовать списковое включение: squares = [x**2 for x in range(10)].
            Функции определяются с помощью ключевого слова def, а классы - с помощью class.
            """,
            metadata={"source": "programming_guide", "language": "python", "topic": "basics"}
        )
        
        # Создаем еще один документ с информацией о веб-разработке
        web_dev_doc = Document(
            page_content="""
            Веб-разработка включает в себя создание веб-сайтов и веб-приложений. Она делится на 
           _frontend_ (клиентская часть) и _backend_ (серверная часть).
            
            Frontend разработка отвечает за пользовательский интерфейс и взаимодействие с пользователем. 
            Основные технологии frontend включают HTML для структуры, CSS для оформления и JavaScript 
            для интерактивности. Современные фреймворки, такие как React, Vue.js и Angular, 
            значительно упрощают создание сложных интерфейсов.
            
            Backend разработка отвечает за серверную логику, базы данных и обработку запросов. 
            Популярные языки backend включают Python (Django, Flask), JavaScript (Node.js), 
            PHP (Laravel), Java (Spring) и другие. Для хранения данных используются различные 
            системы управления базами данных, такие как PostgreSQL, MySQL, MongoDB.
            
            RESTful API - это архитектурный стиль для создания веб-сервисов, которые используют 
            стандартные HTTP методы (GET, POST, PUT, DELETE) для взаимодействия между клиентом и сервером.
            """,
            metadata={"source": "web_development", "topic": "fullstack"}
        )
        
        # Разделение документов на части
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=100,
            length_function=len,
        )
        
        texts = text_splitter.split_documents([programming_doc, web_dev_doc])
        print(f"Документы разделены на {len(texts)} частей")
        
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
        
        # Создание цепочки для поиска и ответов
        # Note: RetrievalQA import may need to be adjusted based on your LangChain version
        # qa_chain = RetrievalQA.from_chain_type(
        #     llm=llm,
        #     chain_type="stuff",
        #     retriever=vectorstore.as_retriever()
        # )
        
        # Примеры вопросов
        questions = [
            "Каковы преимущества языка Python?",
            "Что такое RESTful API?",
            "Какие технологии используются во frontend разработке?"
        ]
        
        print("=== Вопросы и ответы ===")
        # Note: RetrievalQA import may need to be adjusted based on your LangChain version
        print("Note: RetrievalQA functionality is commented out due to import issues")
        print("The vector store and similarity search functionality is still demonstrated below")
        
        # Поиск похожих документов
        print("\n=== Поиск похожих документов ===")
        query = "Что такое фреймворки в Python?"
        similar_docs = vectorstore.similarity_search(query, k=2)
        
        print(f"\nПоиск по запросу: {query}")
        for i, doc in enumerate(similar_docs):
            print(f"\n--- Результат {i+1} ---")
            print(f"Содержимое: {doc.page_content[:200]}...")
            print(f"Метаданные: {doc.metadata}")
        
        # Удаление временной базы данных
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()