from dotenv import load_dotenv
from litellm import Annotated
from pydantic import BaseModel
from langchain_community.utilities import GoogleSerperAPIWrapper
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI

import gradio as gr

load_dotenv(override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
os.getenv("SERPER_API_KEY")
serperSearchApi = GoogleSerperAPIWrapper()
# serperSearchApi.run("What is the capital of France?")


@tool
def tool_search(query: str) -> str:
    """Use Serper Search API to search the web for up-to-date information."""
    return serperSearchApi.run(query)


@tool
def pushNotification(message: str):
    """Push a notification to the user using ntfy"""
    response = requests.post(
        os.getenv("NTFY_URL"),
        data=message,
        headers={"Title": "Task Success"},
    )
    return {"status": response.status_code, "message": "Notification sent successfully"}


tools = [tool_search, pushNotification]


# create state
class State(BaseModel):
    messages: Annotated[list, add_messages]


gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = gemini_llm.bind_tools(tools)
# start the graph builder
graph_builder = StateGraph(State)


# create Node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state.messages)]}


# add nodes
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_conditional_edges("chatbot", tools_condition, "tools")

# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()


def chat(user_input: str, history):
    result = graph.invoke({"messages": [{"role": "user", "content": user_input}]})
    return result["messages"][-1].content


gr.ChatInterface(chat).launch()
