from dotenv import load_dotenv
from pydantic import BaseModel
import gradio as gr
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from pprint import pprint
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")

gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


# create state
class State(BaseModel):
    messages: Annotated[list, add_messages]


# start the graph builder
graph_builder = StateGraph(State)


# create node
def first_node(messages: str) -> str:
    messages = [{"role": "assistant", "content": "hi"}]
    createNode = State(messages=messages)
    return createNode


# add node
graph_builder.add_node("first_node", first_node)

# add edges
graph_builder.add_edge(START, "first_node")
graph_builder.add_edge("first_node", END)

# compile the graph builder
graph_compiler = graph_builder.compile()


def gradio_function(user_input: str, history):
    message = [{"role": "user", "content": user_input}]
    state = State(messages=message)
    result = graph_compiler.invoke(state)
    print(result, flush=True)
    return result["messages"][-1].content


gr.ChatInterface(
    gradio_function,
    title="Simple Chatbot",
).launch()
