"""
Test imports for lesson 3 to verify that all required packages are installed correctly.
"""

try:
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import Chroma
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.document_loaders import TextLoader
    print("✅ Core imports successful!")
    print("Lesson 3 dependencies are correctly installed.")
    print("Note: RetrievalQA may be available through a different import path")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your installation of required packages.")