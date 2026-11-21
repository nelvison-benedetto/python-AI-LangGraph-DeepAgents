from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

def chat_node(state: AgentState) -> dict:
    conversation_history = state["messages"]
    response = llm.invoke(conversation_history)
    return {
        "messages": response
    }

graph = StateGraph(AgentState)
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

agent = graph.compile()

message1 = HumanMessage(content="Hello, my name is NB")

turn1_state = agent.invoke({
    "messages": message1
})

print("--- Graph after first run ---")
print(turn1_state)
print("-"*10)


# --- Graph after first run ---
# {'messages': [HumanMessage(content='Hello, my name is NB', additional_kwargs={}, response_metadata={}, id='b169aec1-2a4f-45d3-bcc4-80d09f636fba'), 
# AIMessage(content='Hello NB! How can I assist you today?', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 10, 'prompt_tokens': 13, 'total_tokens': 23, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0, 'text_tokens': None}, 'prompt_tokens_details': {'audio_tokens': 0, 'cache_write_tokens': None, 'cached_tokens': 0, 'image_tokens': None, 'text_tokens': None}}, 'model_provider': 'openai', 'model_name': 'gpt-4o-2024-08-06', 'system_fingerprint': 'fp_cc22cd67d5', 'id': 'chatcmpl-EmkFVAbjpSWjmEJKrzgOgluAcvTTZ', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--01a1ff65-eb34-7d52-85b4-a63937a5a7a3-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 13, 'output_tokens': 10, 'total_tokens': 23, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}
# ----------  vedi anche tutte le info che ti da l'AI


#### turn2

message2 = HumanMessage(content="What is your favourite movie?")
turn2_state = agent.invoke({
    "messages": turn1_state["messages"] + [message2]  #ai risponde alle 2 domande
})

print("--- Graph after second run ---")
print(turn2_state)
print("-"*10)

