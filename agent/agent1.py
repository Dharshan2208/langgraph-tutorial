# Define the state structure with a list of human message objects
# initialise a gemini model using langchains gemini
# sending and handling diif types of messages
# building and compiling the graph of the agent


# main goal how to integrate llms in our graph

import os
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langgraph.graph import StateGraph, START, END

# Enter your api key
os.environ["GOOGLE_API_KEY"] = ""

class AgentState(TypedDict):
    message : list[HumanMessage]


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

def process(state : AgentState) -> AgentState:
    response = llm.invoke(state["message"])
    print(f"AI : {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,"process")
graph.add_edge("process",END)

agent = graph.compile()


# from IPython.display import Image, display

# image = Image(agent.get_graph().draw_mermaid_png())
# with open("graph.png", "wb") as f:
#     f.write(image.data)
# print("Graph image saved as graph.png")


user_input = input("ENTER : ")
while user_input != "EXIT":
    agent.invoke({"message":[HumanMessage(content=user_input)]})
    user_input = input("ENTER : ")


