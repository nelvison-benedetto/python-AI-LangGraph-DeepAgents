
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated, List, TypedDict

class GraphState(TypedDict):
    input: str
    execution_path: list[str]


def node_a(state:GraphState)->dict:
    print("executing 'node_a'...")
    new_path = state.get("execution_path", []) + ["node_a"]  #[] è fallback, ["node_a"] è semplice text
    return{
        "execution_path": new_path
    }

def node_b(state:GraphState)->dict:
    print("executing 'node_b'...")
    new_path = state.get("execution_path", []) + ["node_b"]  #[] è fallback, ["node_b"] è semplice text
    return{
        "execution_path": new_path
    }


def node_c(state:GraphState)->dict:
    print("executing 'node_c'...")
    new_path = state.get("execution_path", []) + ["node_c"]  #[] è fallback, ["node_a"] è semplice text
    return{
        "execution_path": new_path
    }


def shoud_continue(state:GraphState):  #decide quale nodo eseguire dopo node_a
    print("evaluating conditional edge")
    if "go_to_b" in state["input"]:  #state["input"] non è una str
        print("---> continuing to B")
        return "node_b"
    else:   #se state["input"] non conteneva text 'go_to_b' allora return text "node_c"
        print("---> continuing to C")
        return "node_c"


builder = StateGraph(GraphState)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)

builder.add_edge(START, "node_a")
builder.add_conditional_edges("node_a", shoud_continue)
builder.add_edge("node_b", "node_c")
builder.add_edge("node_c", END)
#quindi visto che non ho text 'go_to_b' in state["input"], allora il flow sarà  START → node_a → [shoud_continue: "node_c"] → node_c → END

graph = builder.compile()


## now testing

initial_state1= {
    "input": "hello langgraph is awesome!"
}

final_state1 = graph.invoke(initial_state1)

print(final_state1)




