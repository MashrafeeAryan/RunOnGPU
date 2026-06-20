import os
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

from runongpu.config import load_config


# Finds the real Google Chrome app on Windows.
# We use real Chrome because Colab login does not like Playwright's default browser.
CHROME_EXE = (
    Path(os.environ["PROGRAMFILES"])
    / "Google"
    / "Chrome"
    / "Application"
    / "chrome.exe"
)

# RunOnGPU's own Chrome profile.
# This saves the user's Colab login without touching their personal Chrome profile.
RUNONGPU_PROFILE_DIR = Path.home() / ".runongpu" / "chrome-profile"

# Local port that lets Playwright control real Chrome.
DEBUG_PORT = 9222

# Starter Colab notebook used when the user does not have their own saved notebook yet.
TEMPLATE_URL = "https://colab.research.google.com/drive/1l8stgex_LpNC4KEYZJQU6RDJgho1YWDM?usp=sharing"


def wait_for_debug_port(timeout_seconds: int = 15) -> None:
    """Wait until Chrome is ready for Playwright to connect."""

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            # If this URL opens, Chrome is listening on the debug port.
            with urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=1):
                return
        except URLError:
            # Chrome may still be starting, so wait a little and try again.
            time.sleep(0.5)

    raise RuntimeError(
        f"Chrome did not open remote debugging port {DEBUG_PORT}. "
        "Close Chrome and try again, or use a different debug port."
    )


def open_colab(notebook_url: str = "") -> str:
    """Open a saved Colab notebook, or copy the template notebook on first run."""

    target_url = notebook_url or TEMPLATE_URL

    # Start real Chrome with a debug port so Playwright can attach to it.
    # The RunOnGPU profile keeps login/session data between runs.
    subprocess.Popen([
        str(CHROME_EXE),
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={RUNONGPU_PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        target_url,
    ])

    # Make sure Chrome is actually ready before Playwright connects.
    wait_for_debug_port()

    with sync_playwright() as playwright:
        # Connect to the Chrome window we just opened.
        browser = playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{DEBUG_PORT}"
        )

        # Use the newest Chrome tab.
        context = browser.contexts[0]
        page = context.pages[-1]

        # Open either the user's saved notebook or the template notebook.
        page.goto(target_url)

        if not notebook_url:
            # First run: copy the shared template into the user's Google Drive.
            while True:
                old_url = page.url

                page.get_by_role("button", name="File", exact=True).click()
                page.get_by_text("Save a copy in Drive").click()

                try:
                    # Success means Colab opened a new Drive notebook, not the login page.
                    page.wait_for_url(
                        lambda url: "colab.research.google.com/drive/" in url
                        and url != old_url
                        and "accounts.google.com" not in url,
                        timeout=30000,
                    )

                    # Colab may open the copied notebook in a new tab, so use the newest tab.
                    page = context.pages[-1]
                    break
                except Exception:
                    input("Please sign into Colab, then press Enter to try again...")

        current_url = page.url

        input("Colab is open. Press Enter when done...")

        browser.close()

        return current_url
    

def write_code_for_github_clone(page):
    #Colab code cells use CodeMirror.
    # .cm-content points to the editable part of each visible code cell
    cell = page.locator(".cm-content").nth(2)
    
    cell.click()
    saved_config = load_config()

    page.keyboard.press("Control+A")
    
    code =  f"""
    folder_name = {saved_config["folder_name"]},
    github_repo_url = {saved_config["repo_url"]}
    !rm -rf {saved_config["folder_name"]}
    !git clone {saved_config["repo_url"]}
    %cd {saved_config["folder_name"]}
        
        
        """
    #Clipboard paste is much faster and more reliable for large code blocks
    page.evaluate("text => navigator.clipboard.writeText(text)", code)
    page.keyboard.press("Control+V")