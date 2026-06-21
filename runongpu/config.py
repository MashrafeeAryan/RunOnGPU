# Confgiuration helpers for RunOnGPU
# This file saves and loads the user's project settings, such as:
# - GitHub repository URL

import json
from pathlib import Path
from rich.console import Console

console = Console()
# Hidden folder in the user's home directory where RunOnGPU stores settings
CONFIG_DIR = Path.home() / ".runongpu"

CONFIG_FILE = CONFIG_DIR/ "config.json"

def save_repo_url(repo_url: str, folder_name: str) -> None:
    CONFIG_DIR.mkdir(exist_ok=True);
    config = {
        "repo_url": repo_url,
        "notebook_url" : "",
        "folder_name" : folder_name
    }
    
    #Writes the url into config.json file
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4);

# Load the saved RunOnGPU configuration from disk
def load_config() -> dict | None:
    if not CONFIG_FILE.exists():
        return None
    #Reads json file and turns it  back into python dictionary
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
#Helper fucntion to save notebook url
def save_notebook_url(notebook_url: str) -> None:
    config = load_config()
    
    if config is None:
        config = {}
    config["notebook_url"] = notebook_url
    
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)
        
        

# Creates a starter runongpu.txt file in the repository.
# This file tells RunOnGPU how to build, test, and run the project.
def create_runongpu_template() -> None:
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

