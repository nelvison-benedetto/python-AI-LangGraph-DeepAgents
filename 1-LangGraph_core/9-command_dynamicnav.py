
from typing import Annotated, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.messages import add_messages

class GraphState(TypedDict):
    temperature: int
    status_message: str
    warning_sent: bool
    final_action_performed: str


def check_temp_node(state:GraphState)->Command[Literal["warn_user", "success"]]:
    temp=state['temperature']
    if temp>90:
        print("---alert: temp to high! issuing command to warn user---")
        return Command(
            update = {
                "status_message": "routing to warning handler...",
                "warning_sent": True
            },
            goto = "warn_user"
        )
    else:
        print("---OK: temp is ok, issuing command to 'success'---")
        return Command(
            update={
                "status_message": "routing to success handler"
            }
        )

def warn_user(state:GraphState):
    print(f"executing 'warn_user': warning successfully sent at {state['temperature']}")
    return {
        "warning": True,
        "final_action_performed": "warning notification sent"
    }

def success(state:GraphState):
    print(f"executing 'success_user': all systems clear")
    return {
        "final_action_performed": "temperature safety confiermed"
    }


builder = StateGraph(GraphState)
builder.add_node(check_temp_node)
builder.add_node(warn_user)
builder.add_node(success)

builder.add_edge(START, "check_temp_node")

### testing

initial_state = {
    "temperature": 100
}

final_state = graph.invoke(initial_state)

print("Final State: ")
print(final_state)


