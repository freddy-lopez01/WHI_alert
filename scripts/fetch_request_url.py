import asyncio
from playwright.async_api import async_playwright, Playwright, Page
import re
from typing import List
import json

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
    return page, browser

async def capture_network_requests(page: Page, url_locations: List[str]):
    """
    Captures all network requests made by the page.

    This function listens to all network requests made by the provided page instance and appends it to a list.

    Parameters:
        page (Page): The Playwright page instance to capture requests from.
    """

    # regex pattern to match URLs in the required form
    url_pattern = re.compile(r"https://locations\.wafflehouse\.com/_next/data/[^/]+/[a-z0-9\-]+\.json\?slug=[a-z0-9\-]+", re.IGNORECASE)
    
    def on_request(request):
        url = request.url
        if url_pattern.match(url) and url not in url_locations:
            url_locations.append(url)
    page.on("request", on_request)

def get_url_location(urls: List[str]) -> List[str]:
    """
    Extract the city, state, and store numbers and stores it into a list.

    Parameters:
        urls (List[str]):

    Returns:
        List[str]:
    """
    slugs = []
    for url in urls:
        match = re.search(r"/([^/]+)\.json", url)
        if match:
            slug = match.group(1)
            slugs.append(slug)
    return slugs


async def scroll_page(page: Page, url_locations: List[str]):
    """
    Scrolls down within the provided HTML locator element dynamically.

    Selects the HTML element and moves cursor to the scrollable area and scrolls a specific number of times. This function runs in parallel with capture_network_requests().

    Parameters:
        page (Page): The Playwright page instance to scroll.
        url_locations (List[str]): The list to store captured URLs.
    """

    scrollable_area = page.locator('[role="feed"][aria-label="list Locations"]')
    await scrollable_area.scroll_into_view_if_needed()
    location_box = await scrollable_area.bounding_box()
    if location_box:
        await page.mouse.move(location_box["x"] + location_box["width"] / 2, location_box["y"] + 10)

    # Note: The current solution to this is to set a specific number of scrolls and each scroll pixel amount (not optimal).
    for _ in range(8400):
        await page.mouse.wheel(0, 90)

async def main():
    # set up Playwright page and browser instance
    page, browser = await setup_browser()
    url_locations = []

    await capture_network_requests(page, url_locations)
    await scroll_page(page, url_locations)
    slugs = get_url_location(url_locations)
    with open("locations.json", "w+") as file:
        json.dump(slugs, file)
    print(f"Total number of locations fetched: {len(slugs)}")

    with open("locations.json", "r") as file:
        slugs = json.load(file)
        print(slugs)

    await asyncio.sleep(2)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())

