# Objective
# Implement a conditional logic to route the flow of data to different nodes
# designing multiple nodes to perform different operations
# Use START and END nodes to manage entry and edn
# creating a router nodes to handle decision making

# main goal is to use add_conditonal_edge

from typing import TypedDict
from langgraph.graph import START,END,StateGraph

class AgentState(TypedDict):
    num1 : int
    operation : str
    num2 : int
    result : int


def adder(state:AgentState) -> AgentState:
    """Adder Function Basically adds """

    state["result"] = state["num1"] + state["num2"]
    return state

def subtracter(state: AgentState) -> AgentState:
    """subtracter Function Basically adds"""

    state["result"] = state["num1"] - state["num2"]
    return

def decide_next_node(state:AgentState)->AgentState:
    """Decide next node of the graph"""

    if(state["operation"]=="+"):
        return "add_operation"

    elif state["operation"] == "-":
        return "sub_operation"


graph = StateGraph(AgentState)

graph.add_node("add_node", adder)
graph.add_node("sub_node", subtracter)
graph.add_node("router",lambda state:state) #Passthrough function

graph.add_edge(START, "router")

graph.add_conditional_edges(
    "router",
    decide_next_node,
    {
        # Edge:Node
        "add_operation":"add_node",
        "sub_operation":"sub_node"
    }
)

graph.add_edge("add_node",END)
graph.add_edge("sub_node",END)

app = graph.compile()


# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")

result = app.invoke({"num1":45, "num2":12,"operation":"+"})
print(result["result"])