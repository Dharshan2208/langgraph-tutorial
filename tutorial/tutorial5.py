# Objective
# Implement a looping logic to route the flow of data back to the nodes
# create a single conditional edge to handle decision making and control
# graph flows

# Main goal is to code a looping logic

from typing import TypedDict
from langgraph.graph import StateGraph,START,END
import random

class AgentState(TypedDict):
    name : str
    number : list[int]
    counter : int

def greeting_node(state : AgentState) -> AgentState:
    """Greeter which says hi"""
    state["name"] = f"Hi Baka {state['name']}"
    state['counter'] = 0

    return state

def random_node(state : AgentState) -> AgentState:
    """Generate some random numbers"""
    state["number"].append(random.randint(0,10))
    state["counter"]+=1
    return state


def should_continue(state : AgentState) -> AgentState:
    """Function to decide what to do next"""

    if(state["counter"] < 5):
        print(f"Entering loop {state["counter"]}")
        return "loop"
    else :
        return "exit"

graph = StateGraph(AgentState)


# greeting-random-random-random-random-random-end


graph.add_node("greeting",greeting_node)
graph.add_node("random",random_node)

graph.add_edge(START, "greeting")
graph.add_edge("greeting","random")

graph.add_conditional_edges(
    "random", #Source Node
    should_continue,  #Action
    {
        "loop":"random",   #Self loop back to node
        "exit":END #end teh graph
    }
)

app = graph.compile()

# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")


result = app.invoke({"name":"Baka","number":[],"counter":-45})
print(result["number"])