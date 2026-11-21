from langgraph.graph import StateGraph, START, END
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages 

class SimpleState(TypedDict):  #ur schema, the nodes will recevive the entire state but return only the ones they edited. 
#puoi definire lo schema con TypeDict(piu leggero e piu utilizzato) / Pydantic BaseModel(aggiunge validazione dei types a runtime, ma è più lento) / dataclass (permette valori di default)
    messages: Annotated[list, add_messages]  #x Annotated add_messages è solo metadata, pero x langgraph lo interpreta come REDUCER x campo messages: grazie a tutto questo ottieni accodamento dei mexs, conversione auto di str in obj (Hello -> HumanMessage(content='Hello')) e assegna ID ad ogni mex! 
    #add_messages (accoda i mexs & conversion & IDs), operator.add (concatena, e.g.list or int)

graph = StateGraph(SimpleState)

def say_hello(state: SimpleState):
    print("Executing say_hello node")
    return {
        "messages": ["Hello","Bye"] 
    }

def say_world(state: SimpleState):
    print("Executing say_world node")
    return {
        "messages": ["Omicron","Perseo 8"] 
    }

graph.add_node("hello_node", say_hello)
graph.add_node("world_node", say_world)

graph.add_edge(START, "hello_node")
graph.add_edge("hello_node", "world_node")
graph.add_edge("world_node", END)

agent = graph.compile()

initial_state = {
    "messages" : []
}
final_state = agent.invoke(initial_state)
print("\n--- Final State ---")
print(final_state)


#print(agent.get_graph().draw_ascii())  #usa lib grandalf. agent.get_graph() ti fa vedere la struttura del ur graph, .draw_ascii() te la disegna come text.


