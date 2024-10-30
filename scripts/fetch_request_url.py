import asyncio
from playwright.async_api import async_playwright, Playwright, Page
import re
from typing import List

async def setup_browser() -> Page:
    """
    Initializes and sets up a Playwright browser instance and a new page

    This function asynchronously starts a Playwright instance and launches a Chromium browser in non-headless mode.
    It opens up a new browser page and nagivates to the WaffleHouse locations website.

    Returns:
        tuple[Page, Browser]: A tuple that contains:
            - Page: The Playwright instance pointing to the specified URL.
            - Browser: A launched browser instance.
    """

    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://locations.wafflehouse.com")
    await browser.close()
    return page, browser

async def capture_network_requests(page: Page) -> List[str]:
    """
    Captures all network requests made by the page.

    This function listens to all network requests made by the provided page instance and appends it to a list.

    Parameters:
        page (Page): The Playwright page instance to capture requests from.

    Returns:
        List[str]: A list of request URLs that were requested by the page.
    """

    # regex pattern to match URLs in the required form
    url_pattern = re.compile(r"https://locations\.wafflehouse\.com/_next/data/[^/]+/[a-z0-9\-]+\.json\?slug=[a-z0-9\-]+", re.IGNORECASE)
    
    url_locations = []
    def on_request(request):
        url = request.url
        if url_pattern.match(url) and url not in url_locations:
            print("Location Request URL:", url)
            url_locations.append(url)
    page.on("request", on_request)
    return url_locations

async def scroll_page():
    """Scrolls down within the provided HTML locator element."""
    # TODO: Locate scrollable area using the locator element.
    # TODO: Move mouse to the scroll area.
    # TODO: Scroll until reaching the bottom of page.
        # Note: The current solution to this is to set a specific number of scrolls and each scroll pixel amount (not optimal).
    pass

async def main():
    """Main function to run script"""
    page, browser = await setup_browser()
    urls = await capture_network_requests(page)
    await asyncio.sleep(10)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

