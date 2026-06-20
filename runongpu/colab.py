import os
import subprocess
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


# Location of the installed Chrome executable on Windows.
# RunOnGPU launches real Chrome instead of Playwright's default browser so it can use
# the user's existing Google/Colab login session.
CHROME_EXE = (
    Path(os.environ["PROGRAMFILES"])
    / "Google"
    / "Chrome"
    / "Application"
    / "chrome.exe"
)

# Location of Chrome's user data folder on Windows.
# This contains browser profiles, cookies, and saved login sessions.
CHROME_USER_DATA_DIR = (
    Path(os.environ["LOCALAPPDATA"])
    / "Google"
    / "Chrome"
    / "User Data"
)

# Local debugging port used by Chrome DevTools Protocol.
# Playwright connects to this port after Chrome starts.
DEBUG_PORT = 9222


def open_colab(notebook_url: str = "") -> str:
    """Open Google Colab in the user's real Chrome profile and return the active URL."""

    # Start Chrome with remote debugging enabled so Playwright can attach to it.
    # The Default profile is used for now because it is usually the user's main profile.
    subprocess.Popen([
        str(CHROME_EXE),
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={CHROME_USER_DATA_DIR}",
        "--profile-directory=Default",
        "https://colab.research.google.com",
    ])

    # Give Chrome enough time to start before Playwright tries to connect.
    time.sleep(5)

    with sync_playwright() as playwright:
        # Attach to the already-running Chrome instance instead of launching a new browser.
        browser = playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{DEBUG_PORT}"
        )

        # Use the existing Chrome context and most recently opened page.
        context = browser.contexts[0]
        page = context.pages[-1]

        # Reopen the saved notebook if one exists; otherwise open Colab home.
        if notebook_url:
            page.goto(notebook_url)
        else:
            page.goto("https://colab.research.google.com")

        current_url = page.url

        input("Colab is open. Press Enter when done...")

        browser.close()

        return current_url