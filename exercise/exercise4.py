from typing import TypedDict
from langgraph.graph import START, END, StateGraph


class AgentState(TypedDict):
    num1: int
    operation: str
    num2: int
    result: int
    num3 : int
    final_result : int


def adder1(state: AgentState) -> AgentState:
    """Adder Function Basically adds"""

    state["result"] = state["num1"] + state["num2"]
    return state


def subtracter1(state: AgentState) -> AgentState:
    """subtracter Function Basically adds"""

    state["result"] = state["num1"] - state["num2"]
    return

def adder2(state: AgentState) -> AgentState:
    """Adder Function Basically adds"""

    state["final_result"] = state["num3"] + state["result"]
    return state


def subtracter2(state: AgentState) -> AgentState:
    """subtracter Function Basically adds"""

    state["final_result"] = state["num3"] - state["result"]
    return


def decide_next_node1(state: AgentState) -> AgentState:
    """Decide next node of the graph"""

    if state["operation"] == "+":
        return "add_operation1"

    elif state["operation"] == "-":
        return "sub_operation1"

def decide_next_node2(state: AgentState) -> AgentState:
    """Decide next node of the graph"""

    if state["operation"] == "+":
        return "add_operation2"

    elif state["operation"] == "-":
        return "sub_operation2"


graph = StateGraph(AgentState)

graph.add_node("add_node1", adder1)
graph.add_node("sub_node1", subtracter1)

graph.add_node("router1", lambda state: state)  # Passthrough function
graph.add_node("router2", lambda state: state)  # Passthrough function

graph.add_node("add_node2", adder2)
graph.add_node("sub_node2", subtracter2)


graph.add_edge(START, "router1")

graph.add_conditional_edges(
    "router1",
    decide_next_node1,
    {
        # Edge:Node
        "add_operation1": "add_node1",
        "sub_operation1": "sub_node1",
    },
)

graph.add_edge("add_node1", "router2")
graph.add_edge("sub_node1", "router2")

graph.add_conditional_edges(
    "router2",
    decide_next_node2,
    {
        # Edge:Node
        "add_operation2": "add_node2",
        "sub_operation2": "sub_node2",
    },
)

graph.add_edge("add_node2",END)
graph.add_edge("sub_node2", END)

app = graph.compile()

# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")

result = app.invoke({"num1": 45, "num2": 12, "operation": "+","num3":43})
print(result["result"],result["final_result"])
