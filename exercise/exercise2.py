from typing import TypedDict, List
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str
    operation: str


def process_values(state: AgentState) -> AgentState:
    if state["operation"] == "+" or state["operation"] == "-":
        result = 0
    elif state["operation"] == "*" or state["operation"] == "/":
        result = 1
    else:
        result = None

    for i in state["values"]:
        if (state["operation"] == "+") :
            result += i
        elif (state["operation"] == "*"):
            result *= i
        elif (state["operation"] == "-"):
            result -= i
        elif (state["operation"] == "/"):
            result /= i

    state["result"] = f"Hi {state['name']}!!! Your Result : {result}"
    return state

graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

# result = app.invoke({"name": "Dharshan", "values": [1, 2, 3, 4, 5, 6],"operation":"*"})

# result = app.invoke(
#     {"name": "Dharshan", "values": [1, 2, 3, 4, 5, 6], "operation": "+"}
# )

result = app.invoke(
    {"name": "Dharshan", "values": [1, 2, 3, 4, 5, 6], "operation": "/"}
)

print(result["result"])



