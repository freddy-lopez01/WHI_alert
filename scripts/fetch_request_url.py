import asyncio
from playwright.async_api import async_playwright, Page, Browser
import re
from typing import List
import json

class WaffleHouseScraper:
    def __init__(self):
        self.url_locations = []
        self.slugs = []

    async def setup_browser(self) -> (Page, Browser):
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
        browser = await playwright.chromium.launch(headless=True) # set headless=False to see browser
        page = await browser.new_page()
        await page.goto("https://locations.wafflehouse.com")
        return page, browser

    async def capture_network_requests(self, page: Page):
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
            if url_pattern.match(url) and url not in self.url_locations:
                self.url_locations.append(url)
        page.on("request", on_request)
        print("Gathered Urls")

    def get_url_location(self, urls: List[str]) -> List[str]:
        """
        Extract the city, state, and store numbers and stores it into a list.

        Parameters:
            urls (List[str]):

        Returns:
            List[str]:
        """
        for url in urls:
            match = re.search(r"/([^/]+)\.json", url)
            if match:
                slug = match.group(1)
                self.slugs.append(slug)
        return self.slugs


    async def scroll_page(self, page: Page):
        """
        Scrolls down within the provided HTML locator element dynamically.

        Selects the HTML element and moves cursor to the scrollable area and scrolls a specific number of times. This function runs in parallel with capture_network_requests().

        Parameters:
            page (Page): The Playwright page instance to scroll.
        """

        scrollable_area = page.locator('[role="feed"][aria-label="list Locations"]')
        await scrollable_area.scroll_into_view_if_needed()
        location_box = await scrollable_area.bounding_box()
        if location_box:
            await page.mouse.move(location_box["x"] + location_box["width"] / 2, location_box["y"] + 10)

        # Note: The current solution to this is to set a specific number of scrolls and each scroll pixel amount (not optimal).
        for _ in range(50):
            await page.mouse.wheel(0, 50)

    async def save_slugs_to_file(self, filename="locations.json"):
        """
        Saves the extracted slugs to a JSON file.
        
        Parameters:
            filename (str): The filename to save the slugs data.
        """
        slugs = self.extract_slugs()
        with open(filename, "w") as file:
            json.dump(slugs, file, ensure_ascii=False, indent=4)
        print(f"Total number of locations fetched: {len(slugs)}")

    async def get_unique_id(self) -> str:
        """
        Extracts the unique ID from a request URL.

        Returns:
            - str: The unique ID as a string.
        """
        url = self.url_locations[0]
        print(url)
        match = re.search(r"/_next/data/([^/]+)/", url)

        if not match:
            print("No unique ID found")
            return ""

        unique_id = match.group(1)
        return unique_id

    async def construct_url(self, unique_id: str):
        """
        Reads from json formatted URLs and replaces the old unique_id with new unique_id and writes to a new file.

        Parameters:
            unique_id (str): Unique ID in string format.
        """
        with open("urls.json", "r") as file:
            urls = json.load(file)

        for url in urls:
            sub = re.sub(r"(_next/data/)[^/]+(/)", rf"\1{unique_id}\2", url)
            self.url_locations.append(sub)

        with open("updated_urls.json", "w") as file:
            json.dump(self.url_locations, file, indent=4)

    async def run(self):
        # set up Playwright page and browser instance
        page, browser = await self.setup_browser()
        await self.capture_network_requests(page)
        #await scroll_page(page, url_locations)
        await asyncio.sleep(1)
        await browser.close()
        unique_id = await self.get_unique_id()
        await self.construct_url(unique_id)
        print(id)

if __name__ == "__main__":
    scraper = WaffleHouseScraper()
    asyncio.run(scraper.run())

