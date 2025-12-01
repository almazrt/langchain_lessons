"""
System Integration Example
This script demonstrates how to integrate LangChain with external systems
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Mock CRM API
class CRMAPI:
    def __init__(self):
        self.customers = {
            "1": {"name": "John Smith", "email": "john@example.com", "status": "VIP"},
            "2": {"name": "Jane Doe", "email": "jane@example.com", "status": "Regular"}
        }
    
    def get_customer_info(self, customer_id):
        customer = self.customers.get(customer_id)
        if customer:
            return f"Name: {customer['name']}, Email: {customer['email']}, Status: {customer['status']}"
        return "Customer not found"
    
    def update_customer_status(self, customer_id, status):
        if customer_id in self.customers:
            self.customers[customer_id]["status"] = status
            return f"Customer {customer_id} status updated to {status}"
        return "Customer not found"

# Mock E-commerce API
class ECommerceAPI:
    def __init__(self):
        self.products = {
            "1": {"name": "Smartphone", "price": 500, "stock": 10},
            "2": {"name": "Laptop", "price": 1000, "stock": 5}
        }
    
    def get_product_info(self, product_id):
        product = self.products.get(product_id)
        if product:
            return f"Product: {product['name']}, Price: ${product['price']}, Stock: {product['stock']}"
        return "Product not found"
    
    def check_inventory(self, product_id):
        product = self.products.get(product_id)
        if product:
            return f"Product {product['name']} inventory: {product['stock']} units"
        return "Product not found"
    
    def process_order(self, product_id, quantity):
        product = self.products.get(product_id)
        if not product:
            return "Product not found"
        
        if product["stock"] >= int(quantity):
            product["stock"] -= int(quantity)
            total = int(quantity) * product["price"]
            return f"Order processed. Total: ${total}. Remaining stock: {product['stock']} units"
        else:
            return f"Insufficient stock. Available: {product['stock']} units"

def create_crm_agent():
    """Create an agent for CRM integration"""
    
    # Initialize APIs
    crm = CRMAPI()
    
    # Create tools
    tools = [
        Tool(
            name="GetCustomerInfo",
            func=lambda customer_id: crm.get_customer_info(customer_id),
            description="Gets customer information by ID"
        ),
        Tool(
            name="UpdateCustomerStatus",
            func=lambda x: crm.update_customer_status(*x.split(",")),
            description="Updates customer status. Format: customer_id,status"
        )
    ]
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt
    prompt = PromptTemplate.from_template("""
    You are a CRM assistant. Help with customer management tasks.
    
    Question: {input}
    {agent_scratchpad}
    """)
    
    # Create agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def create_ecommerce_agent():
    """Create an agent for e-commerce integration"""
    
    # Initialize APIs
    ecommerce = ECommerceAPI()
    
    # Create tools
    tools = [
        Tool(
            name="GetProductInfo",
            func=lambda product_id: ecommerce.get_product_info(product_id),
            description="Gets product information by ID"
        ),
        Tool(
            name="CheckInventory",
            func=lambda product_id: ecommerce.check_inventory(product_id),
            description="Checks product inventory"
        ),
        Tool(
            name="ProcessOrder",
            func=lambda x: ecommerce.process_order(*x.split(",")),
            description="Processes an order. Format: product_id,quantity"
        )
    ]
    
    # Initialize the model
    llm = ChatOpenAI(
        model="openai/gpt-3.5-turbo",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1"
    )
    
    # Create prompt
    prompt = PromptTemplate.from_template("""
    You are an e-commerce assistant. Help with product inquiries and orders.
    
    Question: {input}
    {agent_scratchpad}
    """)
    
    # Create agent
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor

def main():
    """Main function to demonstrate system integrations"""
    try:
        # Check for API key
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Error: OPENROUTER_API_KEY not found in environment variables")
            return
        
        print("=== System Integration Examples ===\n")
        
        # CRM Agent Example
        print("1. CRM Integration:")
        crm_agent = create_crm_agent()
        
        crm_result = crm_agent.invoke({"input": "Show information for customer 1"})
        print(f"CRM Response: {crm_result['output']}\n")
        
        # E-commerce Agent Example
        print("2. E-commerce Integration:")
        ecommerce_agent = create_ecommerce_agent()
        
        ecommerce_result = ecommerce_agent.invoke({"input": "Check inventory for product 1 and process order for 2 units"})
        print(f"E-commerce Response: {ecommerce_result['output']}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()