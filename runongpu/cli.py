# Helps create terminal commands
import typer

#Helps print pretty terminal messages
from rich.console import Console
from runongpu.config import save_repo_url, load_config
app = typer.Typer()

console = Console()

#ALl are commans that can be called using runongpu
@app.command()
def hello():
    console.print("[bold green]RunOnGPU is working.[/bold green]")

@app.command()
def doctor():
    #Checks whether the local RunOnGPU stetup is working
    console.print("[bold cyan]Checking RunOnGPU setup...[/bold cyan]")

    console.print("[green]✓ CLI is running[/green]")
    console.print("[green]✓ Typer is installed[/green]")
    console.print("[green]✓ Rich is installed[/green]")
    
    try:
        import playwright
        console.print("[green]✓ Playwright is installed[/green]")
    except ImportError:
        console.print("[red]✗ Playwright is not installed[/red]")
        console.print("[yellow]Run: pip install playwright[/yellow]")

@app.command()
def init():
    #Saves github repoURl in config file
    repo_url =  typer.prompt("Enter your Github repo URL")
    
    save_repo_url(repo_url)
    
    console.print("[green]✓ Github repo URL saved. [/green]")

@app.command()
def config():
    #Checks if url is saved or not
    repo_url = load_config()
    if repo_url is None:
        console.print("[yellow]No repo url found. Run `runongpu init` first.[/yellow]")
        return
    console.print("[bold cyan]Saved RunOnGPU config:[/bold cyan]")
    console.print(f"GitHub repo URL: [green]{repo_url['repo_url']}[/green]")
if __name__ == "__main__":
    app()