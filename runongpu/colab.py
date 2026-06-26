import os
import subprocess
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

from runongpu.config import load_config

from rich.console import Console

console = Console()
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
TEMPLATE_URL = "https://colab.research.google.com/drive/1pB8iVjR4-tPVSEBFjY8ow6N_F34bcMwi?usp=sharing"


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


def open_colab(notebook_url: str = "", project_config: dict | None = None) -> str:
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


        if not notebook_url:
            while True:
                page.get_by_role("button", name="File", exact=True).click()
                page.get_by_text("Save a copy in Drive").click()

                time.sleep(15)

                # Colab may open the copied notebook in a new tab.
                page = context.pages[-1]

                copied_successfully = (
                    page.url != target_url
                    and "accounts.google.com" not in page.url
                )

                if copied_successfully:
                    break

                input("Please sign into Colab, then press Enter to try again. If already signed in, press enter...")
        current_url = page.url
        if project_config is None:
            raise RuntimeError("project_config was not passed into open_colab().")
        #console.print(f"[green]Notebook URL saved:[/green] {current_url}")
        console.print(f"[cyan]project_config:[/cyan] {project_config}")
        console.print("[cyan]Writing RunOnGPU cell...[/cyan]")
        write_runongpu_cell(page, project_config)
  
        console.print("[green]✓ RunOnGPU cell written[/green]")
        page.get_by_role("button", name="Runtime", exact=True).click()
        page.get_by_role("menuitem", name="Change runtime type").click()
        page.get_by_role("radio", name="T4 GPU").click()
        page.get_by_role("button", name="Save").click()
        page.get_by_role("button", name="Runtime", exact=True).click()
        page.get_by_text("Run allCtrl+F9").click()


        input("Colab is open. Press Enter when done...")

        browser.close()

        return current_url
    

def write_runongpu_cell(page, project_config: dict):
    saved_config = load_config()
    #Colab code cells use Monaco editor.
    # .cm-content points to the editable part of each visible code cell
    # console.print(f"CodeMirror editors: {page.locator('.CodeMirror-code').count()}")
    # console.print(f"Text areas: {page.locator('textarea').count()}")
    editor = page.locator(".monaco-editor").nth(0)
    editor.wait_for(timeout=30000)
    editor.click()

    
    #Grab the commands from the file
    all_commands = (
        project_config["setup"]
        + project_config["build"]
        + project_config["test"]
        + project_config["run"]
    )
    
    command_lines = "\n".join(f"!{command}" for command in all_commands)
    
    page.keyboard.press("Control+A")
    
    code =  f"""folder_name = "{saved_config["folder_name"]}"
github_repo_url = "{saved_config["repo_url"]}"
!rm -rf {saved_config["folder_name"]}
!git clone {saved_config["repo_url"]}
%cd {saved_config["folder_name"]}
{command_lines}
"""

    #Clipboard paste is much faster and more reliable for large code blocks
    page.evaluate("text => navigator.clipboard.writeText(text)", code)
    page.keyboard.press("Control+V")
    
    