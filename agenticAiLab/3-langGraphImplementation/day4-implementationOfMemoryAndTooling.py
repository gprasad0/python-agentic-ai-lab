from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.tools import tool
from langchain_community.utilities import GoogleSerperAPIWrapper
import gradio as gr
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv(override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
os.getenv("SERPER_API_KEY")

search = GoogleSerperAPIWrapper()
conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)
checkpoint_store = SqliteSaver(conn)


# create tools
@tool
def pushNotification(input_message: str) -> str:
    """Push a notification to the user using ntfy"""
    response = requests.post(
        os.getenv("NTFY_URL"),
        data=input_message,
        headers={"Title": "Task Success"},
    )
    return f"Notification sent: {response.status_code}"


@tool
def searchWrapper(query: str) -> str:
    """Searches the web for upto date information"""
    searchedquery = search.run(query)
    return searchedquery


tools = [pushNotification, searchWrapper]
gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

llm_with_tools = gemini_llm.bind_tools(tools)


# create state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# create graph or start the graph builder
graph_builder = StateGraph(State)


# create a node
def first_node(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# add a node
graph_builder.add_node("first_node", first_node)
graph_builder.add_node("tools", ToolNode(tools=tools))
# create edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_conditional_edges("first_node", tools_condition)
graph_builder.add_edge("tools", "first_node")

# compile the graph
graph = graph_builder.compile(checkpointer=checkpoint_store)
config = {"configurable": {"thread_id": 1}}


def chat(user_input: str, history):
    result = graph.invoke(
        {"messages": [{"role": "user", "content": user_input}]}, config=config
    )
    return result["messages"][-1].content


gr.ChatInterface(
    chat,
    title="Simple Chatbot",
).launch()
