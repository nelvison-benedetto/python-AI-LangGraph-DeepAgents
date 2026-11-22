
from typing import List, TypedDict, Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

class SupportState(TypedDict):
    customer_query: str
    query_category: str
    response: str
    tools_used: list[str]

llm = ChatOpenAI(model="gpt-4o")

class QueryClassification(BaseModel):
    category: Literal["billing", "technical", "refund", "general"]
    confidence: float = Field(description="confidence score 0-1")
    reasoning: str = Field(description="why this category was chosen")


def classify_query(state:SupportState)->SupportState:
    print("\n router: analyzing customer query...")
    classifier_llm= llm.with_structured_output(QueryClassification)
    prompt = f"""
    classify the following customers support query into one of these categories: 
    - billing: questions about invoices, payments, charges, pricing
    - technical: technical issues, bugs, feature problems, integration issues
    - refund: refund requests, returns, cancellations
    - account: account access, password reset, profile charges, login issues
    - general: general questions, features inquries, information requests
    customer query: {state['customer_query']}
    classify accurately based on the primary intend.
    """

    classification = classifier_llm.invoke(prompt)
    print(f"category: {classification.category}")
    print(f"confidence: {classification.confidence: .2f}")
    print(f"reasoning: {classification.reasoning}\n")
    return {
        "query_category": classification.category            
    }
    print()

def handle_billing(state:SupportState)->SupportState:
    print("billing handler: processing billing query")
    prompt = f"""
    you are a billing specialist. handle this customer query:
    {state['customer_query']}
    provide a helpful response that:
    - references billing policies and procedures
    - offers to checks their account details
    - provides clear next steps
    - mentions rlevant payment options
    keep it professional and reassuring.
    """
    response = llm.invoke(prompt).content
    return {
        "response": response,
        "tools_used": ["billing_database", "payment_processor"]
    }


def handle_technical(state:SupportState)->SupportState:
    print("technical hanlder: processing technical query")
    prompt=f"""
    you are a technical support specialist. handle this customer query:
    {state['customer_query']}
    provide a helpful response that:
    - offers specific troubleshooting steps
    - references relevant documentation
    - asks clarifying questions if needed
    - provides workarounds if applicable
    be clear and technical but accessible
    """
    response = llm.invoke(prompt).content
    print("technical handler: response generated")
    return {
        "response": response,
        "tools_used": ["knowledge_base", "bug_tracker", "system_logs"]
    }


def handle_refund(state:SupportState)->SupportState:
    print("technical hanlder: processing technical query")
    prompt=f"""
    you are a technical support specialist. handle this customer query:
    {state['customer_query']}
    provide a helpful response that:
    - offers specific troubleshooting steps
    - references relevant documentation
    - asks clarifying questions if needed
    - provides workarounds if applicable
    be clear and technical but accessible
    """
    response = llm.invoke(prompt).content
    print("technical handler: response generated")
    return {
        "response": response,
        "tools_used": ["knowledge_base", "bug_tracker", "system_logs"]
    }

