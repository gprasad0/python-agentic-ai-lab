from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
import gradio as gr

load_dotenv(override=True)


# create state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# create graph or start the graph builder
graph_builder = StateGraph(State)


# create a node
def first_node():
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
