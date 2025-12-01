"""
Business Chatbot Example
This script demonstrates how to create a business chatbot using LangChain
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

def create_business_chatbot():
    """Create a business chatbot with company context"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for business chatbot
    template = """
    You are a helpful assistant for ABC Company. Answer questions based on the company information below:
    
    Company Information:
    - Name: ABC Technology Solutions
    - Services: Software Development, Cloud Consulting, Data Analytics
    - Founded: 2010
    - Employees: 200+
    - Mission: Helping businesses transform through innovative technology solutions
    
    Previous conversation:
    {history}
    
    Customer: {input}
    Assistant:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Create memory
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    
    # Create chain
    chain = prompt | llm | StrOutputParser()
    
    return chain, memory

def main():
    """Main function to demonstrate the business chatbot"""
    try:
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found in environment variables")
            return
        
        # Create chatbot
        chain, memory = create_business_chatbot()
        
        print("Business Chatbot for ABC Company")
        print("Type 'quit' to exit\n")
        
        # Simulate conversation
        questions = [
            "What services does your company offer?",
            "How many employees do you have?",
            "When was the company founded?"
        ]
        
        for question in questions:
            print(f"Customer: {question}")
            
            # Get conversation history
            history = memory.chat_memory.messages
            
            # Get response
            response = chain.invoke({
                "history": history,
                "input": question
            })
            
            print(f"Assistant: {response}\n")
            
            # Save to memory
            memory.save_context({"input": question}, {"output": response})
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()