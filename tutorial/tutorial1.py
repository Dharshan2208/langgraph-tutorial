# Objective
# Understanding and defining the AgentState structure
# Creating a simple node function to process and update state
# Set up a basic langraph structure
# Compile and invoke a langgraph graph
# Understanding how data flows through a single node in langgraph

from typing import Dict,TypedDict

# framework that helps you design and manage the flow of tasks in application
# using a graph
from langgraph.graph import StateGraph


# creating a state
# state schema
class AgentState(TypedDict):
    message : str


def greeting_node(state : AgentState) -> AgentState:
    """Simple Node that adds a greeting message to the state"""

    state["message"] = "Hey " +state["message"]+",how was your day??"

    return state


graph = StateGraph(AgentState)

graph.add_node("greeter", greeting_node)

graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()


# For printing the workflow diagram
# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")

result = app.invoke({"message":"Dharshan"})

print(result["message"])
