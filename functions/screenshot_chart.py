from playwright.sync_api import sync_playwright
import time

def screenshot_chart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        # Load 5-minute candlestick chart
        page.goto("https://www.tradingview.com/chart/?symbol=FX:EURUSD&interval=5", timeout=15000)
        page.wait_for_timeout(2000)  # give JS & chart time to render

        # Save screenshot with timestamp
        timestamp = time.strftime("%Y-%m-%d_%H-%M")
        filename = f"eurusd_{timestamp}.png"
        path = f'screenshots/{filename}'
        page.screenshot(path=path, full_page=True)

        print(f"✅ Saved: {filename}")
        browser.close()
