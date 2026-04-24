import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from pprint import pprint
import asyncio


async def main():
    async_browser = await create_async_playwright_browser(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()
    pprint(tools)
    for tool in tools:
        pprint(f"{tool.name}={tool}")

    tool_dict = {tool.name: tool for tool in tools}
    pprint(tool_dict)
    navigate_tool = tool_dict.get("navigate_browser")
    extract_text_tool = tool_dict.get("extract_text")


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
