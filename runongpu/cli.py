# Builds the command-line interface for RunOnGPU.
import typer

# Prints styled terminal output for a better CLI experience.
from rich.console import Console

# Project helpers for saving local config, creating runongpu.txt, and loading user settings.
from runongpu.config import create_runongpu_template_file, get_folder_name_from_repo_url, save_notebook_url, save_repo_url, load_config
from runongpu.colab import open_colab
from runongpu.parser import parse_config


app = typer.Typer()
console = Console()


@app.command()
def doctor():
    # Verifies that the user's local RunOnGPU setup has the required pieces installed.
    console.print("[bold cyan]Checking RunOnGPU setup...[/bold cyan]")

    console.print("[green]✓ CLI is running[/green]")
    console.print("[green]✓ Typer is installed[/green]")
    console.print("[green]✓ Rich is installed[/green]")

    saved_config = load_config()

    if saved_config is None:
        console.print("[yellow]⚠ No repo URL saved yet[/yellow]")
        console.print("[yellow]Run: runongpu init[/yellow]")
    else:
        console.print("[green]✓ Repo URL is saved[/green]")
        console.print(f"[green] Repo URL: {saved_config["repo_url"]}")

    try:
        import playwright
        console.print("[green]✓ Playwright is installed[/green]")
    except ImportError:
        console.print("[red]✗ Playwright is not installed[/red]")
        console.print("[yellow]Run: pip install playwright[/yellow]")


@app.command()
def init():
    # Store the GitHub repo that RunOnGPU should clone inside Colab.
    repo_url = typer.prompt("Enter your Github repo URL")

    console.print("[yellow]Deriving folder name[/yellow]")
    folder_name = get_folder_name_from_repo_url(repo_url)
    console.print("[green]Successfully derived folder name[/green]")

    save_repo_url(repo_url, folder_name)

    # Create a starter runongpu.txt so users know where to put setup/build/test/run commands.
    create_runongpu_template_file()

    console.print("[green]✓ Github repo URL saved. [/green]")


@app.command()
def config():
    # Show the saved local settings without opening Colab.
    saved_config = load_config()

    if saved_config is None:
        console.print("[yellow]No repo url found. Run `runongpu init` first.[/yellow]")
        return

    console.print("[bold cyan]Saved RunOnGPU config:[/bold cyan]")
    console.print(f"GitHub repo URL: [green]{saved_config['repo_url']}[/green]")

    notebook_url = saved_config.get("notebook_url", "")

    if notebook_url:
        console.print(f"Colab notebook URL: [green]{notebook_url}[/green]")
    else:
        console.print("Colab notebook URL: [yellow]Not saved yet[/yellow]")


@app.command()
def run():
    # Main workflow: parse project commands, open Colab, write the notebook cell, and save the notebook URL.
    saved_config = load_config()

    if saved_config is None:
        console.print("[red]No repo URL saved. Run `runongpu init` first.[/red]")
        return

    try:
        console.print("[yellow]Parsing runongpu.txt. [/yellow]")
        project_config = parse_config()
        console.print("[green] Successfully parsed through runongpu.txt")
    except ValueError as error:
        console.print(f"[red] runongpu.txt error: [/red]\n {error}")
        return

    notebook_url = saved_config.get("notebook_url", "")

    console.print("[bold cyan]Starting RunOnGPU...[/bold cyan]")
    current_notebook_url = open_colab(notebook_url, project_config)

    # Save the copied Colab notebook so future runs reuse it instead of creating another copy.
    save_notebook_url(current_notebook_url)


if __name__ == "__main__":
    app()