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
            
             # Clicks the "New notebook" button on Colab's start page
            page.get_by_text("New notebook").click()

            # Waits until Colab creates/opens the notebook page
            page.wait_for_load_state("networkidle")
        
        current_notebook_url = page.url
        input("Colab is open. Press Enter when you are done...")
        browser.close()
        
        return current_notebook_url
        