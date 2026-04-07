from dotenv import load_dotenv
from litellm import Annotated
from pydantic import BaseModel
from langchain_community.utilities import GoogleSearchAPIWrapper
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.agents import Tool
import os

load_dotenv(override=True)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")

serperSearchApi = GoogleSearchAPIWrapper()
# serperSearchApi.run("What is the capital of France?")

tool_search = Tool(
    name="search",
    func=serperSearchApi.run,
    description="use this tool to search the web for up-to-date information. The input to this tool should be a search query.",
)
tool_search.invoke("What is the capital of France?")


# create state
class State(BaseModel):
    messages: Annotated[list, add_messages]


# start the graph builder
graph_builder = StateGraph(State)
