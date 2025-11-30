import os
import shutil
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
        if os.path.exists("./chroma_db"):
            shutil.rmtree("./chroma_db")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()