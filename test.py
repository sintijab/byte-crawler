import asyncio
import random
from playwright.async_api import async_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36"
]

BASE_URL = "https://www.byte.fm"

from bs4 import BeautifulSoup
import re

async def extract_songs_from_page(page):
    has_playlist = await page.locator(".show-playlist").is_visible()
    if not has_playlist:
        print("No Playlist found on page.")
        return []

    songs = []
    rows = await page.locator(".show-playlist__song").all()
    for row in rows:
        html = await row.inner_html()
        soup = BeautifulSoup(html, "html.parser")

        bold = soup.find("b")
        title = bold.get_text(strip=True) if bold else ""

        full_text = soup.get_text(separator=" ", strip=True)

        if title and title in full_text:
            author = full_text.split(title, 1)[0].strip("–- ").strip()
        else:
            author = full_text

        author = re.sub(r'\s*/\s*', ' ', author)
        
        author = author.strip()

        songs.append({"author": author, "title": title})
    return songs


async def test_first_link_in_broadcast(date_str="2025-05-19"):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--no-sandbox"])
        user_agent = random.choice(USER_AGENTS)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()

        start_url = f"{BASE_URL}/programm/woche/{date_str}/"
        print(f"Opening: {start_url}")
        await page.goto(start_url, wait_until="domcontentloaded", timeout=45000)

        first_cell = page.locator("a.week-cell").first
        if not await first_cell.is_visible():
            print("No week-cell links found.")
            await browser.close()
            return

        await first_cell.click()
        await page.wait_for_selector(".broadcast-show-list__item", timeout=10000)

        show_link = page.locator(".broadcast-show-list__item >> nth=0 >> .show-list-item__texts a[href*='/sendungen/']").first
        if not await show_link.is_visible():
            print("No show link with '/sendungen/' found.")
            await browser.close()
            return

        href = await show_link.get_attribute("href")
        if not href:
            print("No href found in the show link.")
            await browser.close()
            return

        full_url = f"{BASE_URL}{href}" if href.startswith("/") else href
        print(f"Navigating to broadcast page: {full_url}")
        await page.goto(full_url, wait_until="domcontentloaded", timeout=30000)


        songs = await extract_songs_from_page(page)
        print(f"\nFound {len(songs)} songs:")
        for song in songs:
            print(f"- {song['author']} – {song['title']}")

        await browser.close()

asyncio.run(test_first_link_in_broadcast())
