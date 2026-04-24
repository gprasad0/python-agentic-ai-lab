import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Annotated, TypedDict
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import create_async_playwright_browser
from pprint import pprint
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.cnn.com", wait_until="domcontentloaded")
        text = await page.inner_text("body")
        print(text)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
