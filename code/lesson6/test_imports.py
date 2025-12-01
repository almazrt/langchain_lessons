"""
Test imports for lesson 6
This script verifies that all required packages for lesson 6 are installed correctly
"""

try:
    # Core LangChain imports
    from langchain_openai import ChatOpenAI
    from langchain.memory import ConversationBufferMemory
    from langchain.prompts import ChatPromptTemplate, PromptTemplate
    from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
    from langchain_core.pydantic_v1 import BaseModel, Field
    from langchain.agents import Tool, AgentExecutor, create_react_agent
    
    # Utility imports
    import os
    from dotenv import load_dotenv
    from typing import List
    
    print("All imports successful!")
    print("Lesson 6 requirements are satisfied.")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install the required packages:")
    print("pip install langchain==1.1.0 langchain-openai==1.1.0 python-dotenv==1.2.1")