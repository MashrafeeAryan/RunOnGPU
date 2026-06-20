# Confgiuration helpers for RunOnGPU
# This file saves and loads the user's project settings, such as:
# - GitHub repository URL

import json
from pathlib import Path

# Hidden folder in the user's home directory where RunOnGPU stores settings
CONFIG_DIR = Path.home() / ".runongpu"

CONFIG_FILE = CONFIG_DIR/ "config.json"

def save_repo_url(repo_url: str) -> None:
    CONFIG_DIR.mkdir(exist_ok=True);
    config = {
        "repo_url": repo_url,
        "notebook_url" : ""
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