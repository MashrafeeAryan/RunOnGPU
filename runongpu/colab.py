#Helps control chrome
from playwright.sync_api import sync_playwright

def open_colab() -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False
        )
        page = browser.new_page()
        page.goto("https://colab.research.google.com")
        input("Press Enter to close browser...")
        browser.close()
        