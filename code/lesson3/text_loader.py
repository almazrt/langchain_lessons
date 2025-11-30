import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Создаем пример текстового файла
        sample_text = """
        Это пример текстового документа для загрузки в LangChain.
        
        В этом документе мы рассмотрим основные концепции работы с текстовыми файлами
        в рамках фреймворка LangChain. LangChain предоставляет удобные инструменты
        для загрузки, обработки и анализа текстовых данных.
        
        Загрузка документов - первый шаг в процессе работы с внешними данными.
        После загрузки документы могут быть разделены на части, обработаны,
        преобразованы в векторные представления и использованы для различных задач.
        
        TextLoader - это один из самых простых загрузчиков в LangChain.
        Он позволяет загружать текстовые файлы в различных кодировках.
        При загрузке документ сохраняется в формате Document с содержимым
        и метаданными о файле.
        """
        
        # Сохраняем текст в файл
        with open("sample.txt", "w", encoding="utf-8") as f:
            f.write(sample_text)
        
        # Загрузка текстового файла
        loader = TextLoader("sample.txt", encoding="utf-8")
        documents = loader.load()
        
        print(f"Загружено {len(documents)} документов")
        print(f"Содержимое документа:\n{documents[0].page_content}")
        print(f"Метаданные: {documents[0].metadata}")
        
        # Разделение документа на части
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
        )
        
        texts = text_splitter.split_documents(documents)
        print(f"\nДокумент разделен на {len(texts)} частей:")
        
        for i, doc in enumerate(texts):
            print(f"\n--- Часть {i+1} ---")
            print(doc.page_content)
        
        # Удаление временного файла
        if os.path.exists("sample.txt"):
            os.remove("sample.txt")
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()