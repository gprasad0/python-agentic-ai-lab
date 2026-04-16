from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.tools import tool
import gradio as gr
import os
import requests

load_dotenv(override=True)


# create tools
@tool
def pushNotification(input_message: str):
    """Push a notification to the user using ntfy"""
    response = requests.post(
        os.getenv("NTFY_URL"),
        data=input_message,
        headers={"Title": "Task Success"},
    )
    return {"status": response.status_code, "message": "Notification sent successfully"}


@tool
def searchWrapper():
    """Searches the web for upto date information"""


# create state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# create graph or start the graph builder
graph_builder = StateGraph(State)


# create a node
def first_node(messages):
    return "hello"


# add a node
graph_builder.add_node("first_node", first_node)
# create edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

# compile the graph
graph = graph_builder.compile()


def chat():
    # invoke graph
    graph.invoke()


gr.ChatInterface(
    chat,
    title="Simple Chatbot",
).launch()
