import asyncio
from playwright.async_api import async_playwright

async def search_google(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.google.com", wait_until="domcontentloaded")

        try:
            for _ in range(3):
                await page.keyboard.press("Tab")
                await asyncio.sleep(0.3)
            await page.keyboard.press("Enter")
        except Exception as e:
            print(f"Cookie dialog navigation failed: {e}")

        await page.fill("textarea", query)
        await page.keyboard.press("Enter")

        await page.wait_for_selector("h3", timeout=10000)
        print(f"Search for '{query}' completed.")

        await asyncio.sleep(10)
        await browser.close()

# Example usage
asyncio.run(search_google("Radiohead No Surprises"))
