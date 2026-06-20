#Helps control chrome
from playwright.sync_api import sync_playwright

def open_colab(notebook_url: str) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            channel="chrome",
            headless=False
        )
        page = browser.new_page()
        
        if notebook_url:
            page.goto(notebook_url)
        else:
            page.goto("https://colab.research.google.com")
        input("Colab is open. Press Enter when you are done...")
        browser.close()
        