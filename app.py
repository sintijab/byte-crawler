import asyncio
import random
import re
import argparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.94 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
]

BASE_URL = "https://www.byte.fm"

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

        author = re.sub(r'\s*/\s*', ' ', author).strip()
        songs.append({"author": author, "title": title})
    return songs

async def crawl_all_week_cells(date_str):
    all_songs = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--no-sandbox"])

        start_url = f"{BASE_URL}/programm/woche/{date_str}/"
        print(f"Opening: {start_url}")

        temp_context = await browser.new_context(user_agent=random.choice(USER_AGENTS))
        temp_page = await temp_context.new_page()
        await temp_page.goto(start_url, wait_until="domcontentloaded", timeout=45000)

        week_cells = await temp_page.locator("a.week-cell").all()
        cell_count = len(week_cells)
        print(f"Found {cell_count} calendar day(s)")

        await temp_context.close()

        for i in range(cell_count):
            user_agent = random.choice(USER_AGENTS)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()
            print(f"Session nr {i+1} with user-agent: {user_agent[:50]}...")

            await page.goto(start_url, wait_until="domcontentloaded", timeout=45000)
            cells = page.locator("a.week-cell")
            selected_cell = cells.nth(i)

            if not await selected_cell.is_visible():
                print(f"Session #{i+1} is not visible, skipping...")
                await context.close()
                continue

            await selected_cell.click()
            await page.wait_for_timeout(1500)

            try:
                await page.wait_for_selector(".broadcast-show-list__item", timeout=10000)
            except:
                print("No broadcast items found, skipping.")
                await context.close()
                continue

            songs = await extract_songs_from_page(page)
            print(f"Found {len(songs)} songs")
            all_songs.extend(songs)

            await context.close()
            await asyncio.sleep(random.uniform(1.5, 4.0))  # Random delay

        await browser.close()

    print(f"\nTotal songs collected: {len(all_songs)}")
    
    output_file = f"{date_str}.txt"

    with open(output_file, "w", encoding="utf-8") as f:
        for song in all_songs:
            line = f"{song['author']} – {song['title']}"
            print(line)
            f.write(line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", type=str, required=True, help="Date in YYYY-MM-DD format")
    args = parser.parse_args()

    asyncio.run(crawl_all_week_cells(args.date))