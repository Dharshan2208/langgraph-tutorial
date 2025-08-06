# Objective
# Defining a more complex AgentState
# Creating a processing a node that performs opern on list data
# Set up a langraph structure that processes and outputs computed results
# Invoke the graph with structured inputs and retrieve outputs

# Main basically how to handle multiple inputs

import stat
from typing import Type, TypedDict, List
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str


def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""

    state["result"] = f"Hi {state['name']}!!! Your Sum : {sum(state['values'])}"
    return state


graph = StateGraph(AgentState)

graph.add_node("processor", process_values)

graph.set_entry_point("processor")
graph.set_finish_point("processor")

app = graph.compile()

# For printing the workflow diagram
# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")

result = app.invoke({"name":"Dharshan","values":[1,2,3,4,5,6]})

print(result["result"])