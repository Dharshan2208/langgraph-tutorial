# Use different message types - HumanMessage and AIMessage
# Maintaining a full convo history using message types
# creating a sophisticated coversation loop

# main goal : create a form of memory of our agent

import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END

#APi key
os.environ["GOOGLE_API_KEY"] = ""


class AgentState(TypedDict):
    message: list[HumanMessage]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)


def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["message"])
    print(f"AI : {response.content}")
    return state


graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()


# from IPython.display import Image, display

# image = Image(agent.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")


user_input = input("ENTER : ")
while user_input != "EXIT":
    agent.invoke({"message": [HumanMessage(content=user_input)]})
    user_input = input("ENTER : ")
