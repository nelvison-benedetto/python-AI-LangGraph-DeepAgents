
from langgraph.graph import StateGraph, START, END
from typing import Annotated, List, TypedDict
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from dataclasses import dataclass, field


def node_a(state):
    print("executing node A...")
    return {
        "messages": ["Step A completed"],
        "step_count": 1
    }

def node_b(state):
    print("Executing node B...")
    if isinstance(state, dict):
        step_count = state["step_count"]
    else:
        step_count = state.step_count
    print(f"Current step count from state: {step_count}")
    return {
        "messages": ["step B completed"],
        "step_count": 1
    }

def build_and_run_graph(state_schema, initial_state):
    print(f"\n--- Building and Running graph with state schema {state_schema.__name__ if hasattr(state_schema, '__name__') else 'Dictionary'}")
    graph = StateGraph(state_schema)
    graph.add_node("node_a", node_a)
    graph.add_node("node_b",node_b)

    graph.add_edge(START, "node_a")
    graph.add_edge("node_a", "node_b")
    graph.add_edge("node_b", END)

    agent = graph.compile()
    final_state = agent.invoke(initial_state)
    print("\n Final State:")
    print(final_state)
    print("-"*40)


########## using dict semplice (i campi verranno overrides)

def create_dict_state():
    return {
        "messages": [],
        "step_count": 0,
        "private_data": None
    }

#build_and_run_graph(dict, create_dict_state())  


########## using dataclass

@dataclass
class DataclassState:
    messages: Annotated[list, add_messages] = field(default_factory=list)
    step_count: Annotated[int, custom_add] = 0
    private_data: str = ""

build_and_run_graph(DataclassState, DataclassState())

########## using 🔥TypeDict

def custom_add(current: int, new:int) -> int:
    return current + new

class TypeDictState(TypedDict):
    messages : Annotated[List[str], add_messages]
    step_count: Annotated[int, custom_add]
    private_data: str

# build_and_run_graph(TypeDictState, {
#     "messages": [],
#     "step_count": 0,
#     "private_data": ""
# })

########## using Pydantic BaseModel

class PydanticState(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)
    step_count: Annotated[int, custom_add] = Field(default=0)
    private_data: str=Field(default="")

build_and_run_graph(PydanticState, PydanticState())

########################

#     Access in the node| default | validazione | quando usarlo
#dict	     state["x"]	   no	no	solo per prove
#TypedDict	 state["x"]	   no	no	il più usato, leggero
#dataclass	 state.x	   sì	no	se vuoi i default
#Pydantic	 state.x	   sì	sì	se vuoi la validazione dei dati



