from pydantic import BaseModel, Field
from dotenv import load_dotenv
from agents import Agent
import os
from pprint import pprint

load_dotenv(override=True)
geminiApiKey = os.getenv("GOOGLE_GEMINI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_GEMINI_API_KEY")
geminiLlmModel = os.getenv("gemini_llm_model")


class OrchestratorAgentModel(BaseModel):
    reason: str = Field(
        description="Your reasoning for why this search is important to the query."
    )
    query: str = Field(description="The search term to use for the web search.")


class ListOfSearches(BaseModel):
    searches: list[OrchestratorAgentModel] = Field(
        description="A list of web searches to perform to best answer the query."
    )


class OrchestratorAgent:

    async def run(self, query: str):
        searchTerms = await self.searchAgent(query)
        yield searchTerms

    async def searchAgent(self, query: str):
        searches = Agent(
            name="SearchAgent",
            instructions="You are a helpful research assistant. Given a query, come up with a set of web searches to perform to best answer the query. Output 2 terms to query for",
            model=geminiLlmModel,
            output_type=ListOfSearches,
        )
        pprint(searches)
        return searches.final_output.searches
