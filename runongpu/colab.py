import os
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright


# Path to the installed Google Chrome executable on Windows.
# RunOnGPU uses real Chrome instead of Playwright's bundled Chromium because
# Google Colab login can block automated/unknown browsers.
CHROME_EXE = (
    Path(os.environ["PROGRAMFILES"])
    / "Google"
    / "Chrome"
    / "Application"
    / "chrome.exe"
)

# Dedicated Chrome profile for RunOnGPU.
# This keeps RunOnGPU separate from the user's personal Chrome profile while
# still allowing login cookies/session data to persist across runs.
RUNONGPU_PROFILE_DIR = Path.home() / ".runongpu" / "chrome-profile"

# Local Chrome DevTools Protocol port.
# Chrome opens this local-only port so Playwright can attach to the real browser.
DEBUG_PORT = 9222

# Shared starter notebook used when the user does not have a saved notebook yet.
TEMPLATE_URL = "https://colab.research.google.com/drive/1l8stgex_LpNC4KEYZJQU6RDJgho1YWDM?usp=sharing"


def wait_for_debug_port(timeout_seconds: int = 15) -> None:
    """Wait until Chrome exposes its local DevTools endpoint."""

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            with urlopen(f"http://127.0.0.1:{DEBUG_PORT}/json/version", timeout=1):
                return
        except URLError:
            time.sleep(0.5)

    raise RuntimeError(
        f"Chrome did not open remote debugging port {DEBUG_PORT}. "
        "Close Chrome and try again, or use a different debug port."
    )


def open_colab(notebook_url: str = "") -> str:
    """Open an existing Colab notebook or create a Drive copy from the template."""

    target_url = notebook_url or TEMPLATE_URL

    # Start real Chrome with remote debugging enabled.
    # The custom user-data-dir gives RunOnGPU its own reusable browser profile.
    subprocess.Popen([
        str(CHROME_EXE),
        f"--remote-debugging-port={DEBUG_PORT}",
        f"--user-data-dir={RUNONGPU_PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        target_url,
    ])

    # Do not guess with sleep alone; verify Chrome is actually ready for CDP.
    wait_for_debug_port()

    with sync_playwright() as playwright:
        # Attach Playwright to the real Chrome session through CDP.
        browser = playwright.chromium.connect_over_cdp(
            f"http://127.0.0.1:{DEBUG_PORT}"
        )

        # Use the active Chrome context and the newest tab opened by RunOnGPU.
        context = browser.contexts[0]
        page = context.pages[-1]

        page.goto(target_url)

        # If no notebook has been saved yet, copy the shared template into
        # the user's Google Drive so future runs can reuse their own notebook.
        if not notebook_url:
            page.get_by_role("button", name="File", exact=True).click()
            page.get_by_text("Save a copy in Drive").click()

        current_url = page.url

        input("Colab is open. Press Enter when done...")

        browser.close()

        return current_url