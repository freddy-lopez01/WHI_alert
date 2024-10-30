import pytest
from playwright.async_api import async_playwright, expect


@pytest.mark.asyncio
async def test_has_title():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://locations.wafflehouse.com/")
        await expect(page).to_have_title("WaffleHouse")
