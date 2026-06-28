# Configuration helpers for RunOnGPU.
# This file manages small local settings that should persist between CLI runs,
# such as the GitHub repository URL and the copied Colab notebook URL.

import json
from pathlib import Path
from rich.console import Console

console = Console()

# Store RunOnGPU settings in the user's home directory instead of the project repo.
# This keeps personal/local state out of Git.
CONFIG_DIR = Path.home() / ".runongpu"

CONFIG_FILE = CONFIG_DIR / "config.json"


def save_repo_url(repo_url: str, folder_name: str) -> None:
    CONFIG_DIR.mkdir(exist_ok=True)
    config = {
        "repo_url": repo_url,
        "notebook_url": "",
        "folder_name": folder_name
    }

    # Persist the selected project so future `runongpu run` calls know what to clone.
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def load_config() -> dict | None:
    # Return None when the user has not run `runongpu init` yet.
    if not CONFIG_FILE.exists():
        return None

    # Convert the saved JSON config back into a Python dictionary.
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_notebook_url(notebook_url: str) -> None:
    # Keep the copied Colab notebook URL so RunOnGPU reuses it instead of
    # creating a new notebook copy every time.
    config = load_config()

    if config is None:
        config = {}

    config["notebook_url"] = notebook_url

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def create_runongpu_template_file() -> None:
    # Create a starter runongpu.txt in the current project folder.
    # The file documents the command sections that RunOnGPU later parses.
    txt_path = Path("runongpu.txt")

    if not txt_path.exists():

        txt_path.write_text(
            """# RunOnGPU Configuration
#
# Add one command per line under each section.
# Empty sections are allowed.
#
# Example Python project:
#
# [setup]
# pip install -r requirements.txt
#
# [run]
# python main.py
#
# Example CUDA project:
#
# [build]
# nvcc main.cu -o main
#
# [run]
# ./main
#
# Example CMake project:
#
# [build]
# cmake -S . -B build
# cmake --build build
#
# [run]
# ./build/my_program

[setup]

[build]

[test]

[run]
""",
            encoding="utf-8",
        )
        console.print("[green]✓ Added runongpu.txt to the repo. [/green]")
    else:
        console.print("[yellow] runongpu.txt already exists. Good job following instructions! Proud of you! [/yellow]")


def get_folder_name_from_repo_url(repo_url: str) -> str:
    # Git clones repositories into a folder named after the repo, so derive that
    # folder name from the URL instead of asking the user to type it manually.
    return repo_url.rstrip("/").split("/")[-1].replace(".git", "")