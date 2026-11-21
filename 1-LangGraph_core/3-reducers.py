from langgraph.graph import StateGraph,  END, START
from typing import Annotated, List, TypedDict


class StateWithoutReducers(TypedDict):
    count: int
    animals: List[str]

def node_to_update(state: StateWithoutReducers) -> dict:
    return{
        "count":1,
        "animals": ["cat"]
    }

initial_state = {
    "count": 5,
    "animals": ["lion", "buffalo"]
}


def run_example(name: str, state_schema:type, node_func:callable, initial_state:dict):

    print(f"--- Running Example {name} ---")
    graph = StateGraph(state_schema)
    graph.add_node("update_node", node_func)
    graph.add_edge(START, "update_node")
    graph.add_edge("update_node", END)

    app = graph.compile()
    final_state = app.invoke(initial_state)
    print(f"Initial State: {initial_state}")
    print(f"Final State: {final_state}")
    print("-"*40)


run_example(
    name="No reducer", 
    state_schema=StateWithoutReducers, 
    node_func=node_to_update,
    initial_state=initial_state
    )


################ with Reducers

def update_count(current, new):
    return current + new

class StateWithReducers(TypedDict):
    count: Annotated[int, update_count]
    animals: Annotated[List[str], add]

run_example(
    name="With Reducers",
    state_schema=StateWithoutReducers,
    node_func=node_to_update,
    initial_state=initial_state
)
