from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from typing import Annotated, List, TypedDict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage, BaseMessage

class MyGraphState(MessagesState):
    turn_count: int

def user_node(state=MyGraphState)->dict:
    print("Executing 'user_node'...")
    return{
        "messages": HumanMessage(content="openai is the best company in the world!")
    }


def ai_node(state: MyGraphState):
    print("Executing 'ai_node'...")
    last_message = state["messages"][-1].content
    print(f"Human prompt: {last_message}")
    response_content = f"I have received ur mex {last_message} however I am a fake response and can't responde.\n But at least my code is working"
    return {
        "messages": AIMessage(content=response_content)
    }

def counter_node(state:MyGraphState):
    print(f"executing 'counter_node'...")
    return {
        "turn_count": state["turn_count"]+1
    }

graph = StateGraph(MyGraphState)

graph.add_node(user_node)
graph.add_node(ai_node)
graph.add_node(counter_node)

graph.add_edge(START, "user_node")
graph.add_edge("user_node", "ai_node")
graph.add_edge("ai_node", "counter_node")
graph.add_edge("counter_node", END)

agent = graph.compile()

initial_state = {
    "turn_count": 0
}

final_state = agent.invoke(initial_state)
print("--- Final State ---")
print(final_state)




