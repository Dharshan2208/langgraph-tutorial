from ast import List
from typing import TypedDict
from langgraph.graph import StateGraph


class AgentState(TypedDict):
    name: str
    age: str
    final: str
    skills : List


def first_node(state: AgentState) -> AgentState:
    """First node of the sequence"""

    state["final"] = f"Hi {state['name']}"
    return state


def second_node(state: AgentState) -> AgentState:
    """Second node of the sequence"""

    state["final"] = state["final"] + f" You are {state['age']} years old!!!"
    return state

def third_node(state:AgentState) -> AgentState:
    """Third node of the sequence"""
    skills = ""
    for i in state["skills"]:
        skills += i+" "

    state["final"] = state["final"] + f" You have these skills  : {skills}."
    return state



graph = StateGraph(AgentState)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.set_entry_point("first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.set_finish_point("third_node")

app = graph.compile()

# from IPython.display import Image, display

# image = Image(app.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")

result = app.invoke({"name": "Chifuyu", "age": 19 , "skills" :["ML","GenAI","Go"]})
print(result["final"])
