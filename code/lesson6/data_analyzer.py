"""
Data Analyzer Example
This script demonstrates how to analyze data and documents using LangChain
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

# Load environment variables
load_dotenv()

class ReviewAnalysis(BaseModel):
    sentiment: str = Field(description="Overall sentiment: positive, negative, or neutral")
    key_points: List[str] = Field(description="Key points from the review")
    suggestions: List[str] = Field(description="Suggestions for improvement")

class LegalAnalysis(BaseModel):
    obligations: List[str] = Field(description="Legal obligations of the parties")
    risks: List[str] = Field(description="Potential risks identified")
    recommendations: List[str] = Field(description="Recommendations for improvement")

def create_review_analyzer():
    """Create a customer review analyzer"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for review analysis
    review_template = """
    Analyze the following customer review and provide a structured response:
    
    Review: {review}
    
    {format_instructions}
    """
    
    # Create JSON parser
    parser = JsonOutputParser(pydantic_object=ReviewAnalysis)
    
    review_prompt = PromptTemplate(
        template=review_template,
        input_variables=["review"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create chain
    review_chain = review_prompt | llm | parser
    
    return review_chain

def create_legal_analyzer():
    """Create a legal document analyzer"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for legal analysis
    legal_template = """
    You are a legal expert. Analyze the following document and identify key legal aspects:
    
    Document:
    {document}
    
    Analyze:
    1. Legal obligations of the parties
    2. Potential risks
    3. Recommendations for improvement
    
    {format_instructions}
    """
    
    # Create JSON parser
    parser = JsonOutputParser(pydantic_object=LegalAnalysis)
    
    legal_prompt = PromptTemplate(
        template=legal_template,
        input_variables=["document"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create chain
    legal_chain = legal_prompt | llm | parser
    
    return legal_chain

def main():
    """Main function to demonstrate data analyzers"""
    try:
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found in environment variables")
            return
        
        print("=== Data Analysis Examples ===\n")
        
        # Analyze customer review
        print("1. Customer Review Analysis:")
        review_chain = create_review_analyzer()
        
        review = "The product arrived quickly, but the quality is disappointing. The packaging was damaged."
        
        review_result = review_chain.invoke({"review": review})
        
        print(f"Sentiment: {review_result['sentiment']}")
        print("Key Points:")
        for point in review_result['key_points']:
            print(f"  - {point}")
        print("Suggestions:")
        for suggestion in review_result['suggestions']:
            print(f"  - {suggestion}")
        print()
        
        # Analyze legal document
        print("2. Legal Document Analysis:")
        legal_chain = create_legal_analyzer()
        
        contract = """
        SUPPLY AGREEMENT
        1. Supplier shall deliver goods within 30 days.
        2. Buyer shall pay within 10 days of receipt.
        3. Late delivery penalty: 0.1% of goods value per day.
        """
        
        legal_result = legal_chain.invoke({"document": contract})
        
        print("Legal Obligations:")
        for obligation in legal_result['obligations']:
            print(f"  - {obligation}")
        print("Potential Risks:")
        for risk in legal_result['risks']:
            print(f"  - {risk}")
        print("Recommendations:")
        for recommendation in legal_result['recommendations']:
            print(f"  - {recommendation}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()