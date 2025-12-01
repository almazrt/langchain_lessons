"""
Content Generator Example
This script demonstrates how to create content generators using LangChain
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

class MarketingContent(BaseModel):
    headline: str = Field(description="Attention-grabbing headline")
    body: str = Field(description="Main content body")
    call_to_action: str = Field(description="Call to action statement")

def create_ad_generator():
    """Create an advertising content generator"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.7
    )
    
    # Create prompt template for ad generation
    ad_template = """
    Create compelling marketing content for a product "{product}".
    Target audience: {audience}
    Key benefits: {benefits}
    Tone: {tone}
    
    {format_instructions}
    """
    
    # Create JSON parser for structured output
    parser = JsonOutputParser(pydantic_object=MarketingContent)
    
    ad_prompt = PromptTemplate(
        template=ad_template,
        input_variables=["product", "audience", "benefits", "tone"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    # Create chain
    ad_chain = ad_prompt | llm | parser
    
    return ad_chain

def create_report_generator():
    """Create a report generator"""
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt template for report generation
    report_template = """
    Analyze the following data and create a professional report:
    
    Data:
    {data}
    
    Requirements:
    - Format: {format}
    - Length: {length}
    - Focus on: {focus}
    
    Report:
    """
    
    report_prompt = PromptTemplate.from_template(report_template)
    
    # Create chain
    report_chain = report_prompt | llm | StrOutputParser()
    
    return report_chain

def main():
    """Main function to demonstrate content generators"""
    try:
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found in environment variables")
            return
        
        print("=== Content Generation Examples ===\n")
        
        # Generate marketing content
        print("1. Marketing Content Generation:")
        ad_chain = create_ad_generator()
        
        ad_result = ad_chain.invoke({
            "product": "Smart Water Bottle",
            "audience": "Fitness enthusiasts",
            "benefits": "Tracks water intake, reminds to hydrate, eco-friendly",
            "tone": "energetic and motivational"
        })
        
        print(f"Headline: {ad_result['headline']}")
        print(f"Body: {ad_result['body']}")
        print(f"Call to Action: {ad_result['call_to_action']}\n")
        
        # Generate report
        print("2. Report Generation:")
        report_chain = create_report_generator()
        
        sales_data = """
        January: 100 units, revenue $10,000
        February: 120 units, revenue $12,000
        March: 150 units, revenue $15,000
        """
        
        report_result = report_chain.invoke({
            "data": sales_data,
            "format": "executive summary",
            "length": "1 paragraph",
            "focus": "growth trends"
        })
        
        print("Sales Report:")
        print(report_result)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()