from typing import Dict,TypedDict
from unittest import result

from langgraph.graph import StateGraph

class AgentState(TypedDict):
    name: str


def compliment_node(state: AgentState) -> AgentState:
    """Simple Node that add compliements to name"""

    state["name"] += ",You are very genius baka you should go and touch some grass."
    return state

graph = StateGraph(AgentState)

graph.add_node("complimenter", compliment_node)

graph.set_entry_point("complimenter")
graph.set_finish_point("complimenter")

app = graph.compile()

result = app.invoke({"name":"Chifuyu"})
print(result["name"])
