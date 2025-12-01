"""
Educational Application Example
This script demonstrates how to create educational applications using LangChain
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

class Question(BaseModel):
    question: str = Field(description="The question")
    options: List[str] = Field(description="Answer options")
    correct_answer: str = Field(description="Correct answer")

class Quiz(BaseModel):
    questions: List[Question] = Field(description="List of questions")

def create_tutorial_generator():
    """Create a tutorial generator"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for tutorial generation
    tutorial_template = """
    Create educational material on "{topic}" for "{level}" level learners.
    
    Requirements:
    - Format: {format}
    - Length: {length}
    - Include examples: {examples}
    - Style: {style}
    
    Educational material:
    """
    
    tutorial_prompt = PromptTemplate.from_template(tutorial_template)
    
    # Create chain
    tutorial_chain = tutorial_prompt | llm | StrOutputParser()
    
    return tutorial_chain

def create_quiz_generator():
    """Create a quiz generator"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for quiz generation
    quiz_template = """
    Create a quiz with {num_questions} questions on "{topic}" for "{level}" level.
    
    {format_instructions}
    """
    
    # Create JSON parser
    parser = JsonOutputParser(pydantic_object=Quiz)
    
    quiz_prompt = PromptTemplate(
        template=quiz_template,
        input_variables=["num_questions", "topic", "level"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create chain
    quiz_chain = quiz_prompt | llm | parser
    
    return quiz_chain

def main():
    """Main function to demonstrate educational applications"""
    try:
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found in environment variables")
            return
        
        print("=== Educational Application Examples ===\n")
        
        # Generate tutorial
        print("1. Tutorial Generation:")
        tutorial_chain = create_tutorial_generator()
        
        tutorial_result = tutorial_chain.invoke({
            "topic": "Python basics",
            "level": "beginner",
            "format": "step-by-step guide",
            "length": "3 paragraphs",
            "examples": "yes",
            "style": "friendly and clear"
        })
        
        print("Python Basics Tutorial:")
        print(tutorial_result)
        print()
        
        # Generate quiz
        print("2. Quiz Generation:")
        quiz_chain = create_quiz_generator()
        
        quiz_result = quiz_chain.invoke({
            "num_questions": "3",
            "topic": "machine learning",
            "level": "beginner"
        })
        
        print("Machine Learning Quiz:")
        for i, question in enumerate(quiz_result['questions'], 1):
            print(f"{i}. {question['question']}")
            for j, option in enumerate(question['options'], 1):
                print(f"   {j}) {option}")
            print(f"   Correct answer: {question['correct_answer']}\n")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()