
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
    print("technical hanlder: processing refund query...")
    prompt=f"""
    you are a technical support specialist. handle this customer query:
    {state['customer_query']}
    provide a helpful response that:
    - explains the refund policy clearly
    - outlines the refund process and timeline
    - asks for necessary information (order number, reason, ect)
    - shows empathy and understanding
    be empathetic and solution-focused
    """
    response = llm.invoke(prompt).content
    print("refund handler: response generated")
    return {
        "response": response,
        "tools_used": ["order_database", "refund_processor"]
    }

def handle_general(state:SupportState)->SupportState:
    print("general handler: processing general inquiry...")
    prompt=f"""
    you are a general support specialist. handle this customer query:
    {state['customer_query']}
    provide a helpful response that:
    - answers their question clearly 
    - provides relevant links or resources
    - offers additional help if needed
    - suggests related feat they might find useful
    be friendly and informative
    """
    response = llm.invoke(prompt).content
    print("general handler: response generated\n")
    return {
        "response": response,
        "tools_used": ["knowledge_base", "faq_database"]
    }


def route_query(state:SupportState)->Literal["billing","technical", "refund","general"]:
    print(f"routing: directing to {state['query_category']} handler...\n")
    return state['query_category']


builder = StateGraph(SupportState)
builder.add_node("classify_query", classify_query)
builder.add_node("billing",handle_billing)
builder.add_node("technical", handle_technical)
builder.add_node("refund", handle_refund)
builder.add_node("general", handle_general)

builder.add_edge(START, "classify_query")
builder.add_conditional_edges(
    "classify_query",
    route_query,
    {
        "billing": "billing",
        "technical": "technical",
        "refund": "refund",
        "general": "general"
    }
)

builder.add_edge("billing", END)
builder.add_edge("technical", END)
builder.add_edge("refund", END)
builder.add_edge("general", END)

graph = builder.compile()

billing_prompt = "i was charged twice for my subscription this month. can u help me?"
technical_prompt = "the app keeps crashing when i try to upload files larger than 10MB"
refund_prompt = "i'd like to request a refund for my recent purchase. it doesn't meet my needs."
general_prompt = "what feat are included in the pro plan"

result = graph.invoke({
    "customer_query": billing_prompt,
    "query_category": "",
    "response": "",
    "tools_used": ""
})

print(f"="*10)
print(f"final response ({result['query_category'].upper()})")
print(result['response'])
print(f"\n tools used: {','.join(result['tools_used'])}")



