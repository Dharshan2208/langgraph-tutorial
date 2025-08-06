from csv import Error
from os import system
from sys import exception
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage  # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage  # Message for providing instructions to the LLM
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


load_dotenv()

# Gloabla variable storing documents content
document_content = ""


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content :str) -> str:
    """Update the document with the provided content"""
    global document_content
    document_content = content

    return f"Document has been updated successfully !!! Current content is: \n{document_content}"


@tool
def save(filename :str) -> str:
    """SAve the current documnet to a text file and finsih teh process

    Args:
        filename:Name of teh textfile
    """

    global document_content

    if not filename.endswith('.txt'):
        filename=f"{filename}.txt"

    try:
        with open(filename,'w') as file:
            file.write(document_content)

        print(f"Documnet has been saved to {filename}")
        return f"Document has been saved successfully to {filename}"

    except Exception as e:
        return f"Error {str(e)}"


tools = [update, save]


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7).bind_tools(tools)

def our_agent(state : AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
        You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.

        - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
        - If the user wants to save and finish, you need to use the 'save' tool.
        - Make sure to always show the current document state after modifications.

        The current document content is:{document_content}
        """)


    if not state["messages"]:
        user_input = "I'm ready to help you a update a document .What would you like to create???"
        user_message = HumanMessage(content=user_input)


    else:
        user_input = input("What would you like to do with the document??")
        print(f"\n USER : {user_input}")
        user_message = HumanMessage(content=user_input)


    all_mesasages = [system_prompt] + list(state["messages"]) + [user_message]

    response = model.invoke(all_mesasages)

    print(f"AI : {response.content}")

    if hasattr(response,"tool_calls") and response.tool_calls:
        print(f"USING TOOLS : {[tc['name'] for tc in response.tool_calls]}")


    return {"messages" : list(state["messages"]) + [user_message, response]}


def should_continue(state:AgentState)->str:
    """Determine if we shold continue or end the conversation"""

    messages = state["messages"]

    if not messages:
        return "continue"

    # THis looks for the most recent tool message

    for message in reversed(messages):
        # ....and checks if this is a ToolMessage rsulting from save

        if(isinstance(message,ToolMessage)and
        "saved" in message.content.lower() and
        "document" in message.content.lower()):
            return "end" #goes to the end edge which leads to the endpoint


    return "continue"


def print_message(messages):
    """Fucntion to print the messages in more readable format"""
    if not messages:
        return

    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"Tool Result : {message.content}")



graph  = StateGraph(AgentState)

graph.add_node("agent",our_agent)
graph.add_node('tools',ToolNode(tools))


graph.set_entry_point("agent")
graph.add_edge("agent","tools")

graph.add_conditional_edges(
    "tools",
    should_continue,{
        "continue":"agent",
        "end":END,
    },
)

app = graph.compile()

def run_doc_agent():
    print("\n ========== DRAFTER =========")

    state = {"messages":[]}

    for step in app.stream(state,stream_mode="values"):
        if "messages" in step:
            print_message(step["messages"])

    print("\n ======= DRAFTER FINISHED")


if __name__ == "__main__":
    run_doc_agent()