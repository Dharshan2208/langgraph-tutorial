from sys import exception
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class for all message types in LangGraph
from langchain_core.messages import ToolMessage # Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import SystemMessage # Message for providing instructions to the LLM
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


load_dotenv()

# Annotated - provides additional context without affecting the type itself

# Sequence - to automatically handle the state updates for sequences succh as by adding new
# messages to a chat history

# Reducer Function

# Rule that controls how updates from nodes are combined with the existing state;
# tells us how to merge new data into the current state

# without a reducer , updates would have replaced the existing value entirely.

# Example
# Without a reducer
# state = {"messages":["Hi!!!"]}
# update = {"messages": ["Nice to meet you"]}
# result = {"messages": ["Nice to meet you"]}

# With a reducer
# state = {"messages": ["Hi!!!"]}
# update = {"messages": ["Nice to meet you"]}
# result = {"messages": ["Hi!!!,Nice to meet you"]}


class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]


@tool
def add(a:int,b:int):
    """This is a an addition fucntion that adds two numbers """
    return a + b

@tool
def subtract(a:int,b:int):
    """This is a subtraction fiunciton that subtract two numbers"""
    return a - b

@tool
def multiply(a: int, b: int):
    """This is a multiplication fiunciton that mulitply two numbers"""
    return a * b


@tool
def divide(a: int, b: int):
    """This is a multiplication fiunciton that divide two numbers"""
    if(b == 0):
        return exception("Can't divide by 0")

    return a / b


tools = [add,multiply,subtract,divide]


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7).bind_tools(tools)

def model_call(state:AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI Assistant,please answer my query to your best knowledge."
    )
    # response = model.invoke(["You are my assistant, please answer my query to the best of your abillity"])
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages":[response]}

def should_continue(state:AgentState):
    messages = state["messages"]
    last_message=messages[-1]

    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"


graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)


graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue":"tools",
        "end":END
    }
)

graph.add_edge("tools","our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()


# inputs = {"message":[{"user","Add 60+34 and then mulitply the result by 12,Also tell me a dad as well as a dark joke please"}]}
inputs = {
    "messages": [
        HumanMessage(
            # content="Add 60+34 and then multiply the result by 12. Also tell me few dad joke please"
            content="Add 60+34,Subtract 4567+9830,Divide 970 adn 45,Mulitply 53 and 47.And also tell me few dad jokes which are too funny.."
        )
    ]
}

print_stream(app.stream(inputs, stream_mode="values"))

