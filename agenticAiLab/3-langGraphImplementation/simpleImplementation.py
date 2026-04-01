from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from pydantic import BaseModel
import gradio as gr
import random

load_dotenv(override=True)

nouns = [
    "Cabbages",
    "Unicorns",
    "Toasters",
    "Penguins",
    "Bananas",
    "Zombies",
    "Rainbows",
    "Eels",
    "Pickles",
    "Muffins",
]
adjectives = [
    "outrageous",
    "smelly",
    "pedantic",
    "existential",
    "moody",
    "sparkly",
    "untrustworthy",
    "sarcastic",
    "squishy",
    "haunted",
]


# create state
class State(BaseModel):
    # add_messages is the reduceer -> concatenates the messsages
    messages: Annotated[list, add_messages]


# start the graph builder with state
graph_builder = StateGraph(State)


# create a node
def first_node(old_state: State) -> State:
    reply = f"{random.choice(nouns)} are {random.choice(adjectives)}"
    messages = [{"role": "assistnat"}, {"content": reply}]
    newState = State(messages=messages)
    return newState


# add a node
graph_builder.add_node("first_node", first_node)

# create edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

# compile graph
graph = graph_builder.compile()

def chat(user_input:str,history):
    