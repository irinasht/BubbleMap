import asyncio
from playwright.async_api import async_playwright

async def get_screenshot():
    url = "https://app.bubblemaps.io/sol/token/JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=[
            '--start-maximized',
            '--disable-blink-features=AutomationControlled'
        ])

        context = await browser.new_context(
            user_agent=user_agent,
            viewport={'width': 1920, 'height': 1080},
        )

        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(20000)

        await page.screenshot(path="bubblemaps_final_5.png", full_page=True)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(get_screenshot())
