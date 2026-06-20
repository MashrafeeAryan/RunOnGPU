# Helps create terminal commands
import typer

#Helps print pretty terminal messages
from rich.console import Console
from runongpu.config import save_notebook_url, save_repo_url, load_config
from runongpu.colab import open_colab
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
    saved_config = load_config()

    if saved_config is None:
        console.print("[yellow]⚠ No repo URL saved yet[/yellow]")
        console.print("[yellow]Run: runongpu init[/yellow]")
        
    else:
        console.print("[green]✓ Repo URL is saved[/green]")
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
    #Run the saved github repo cuda code on GoogleColab
    saved_config = load_config()
    if saved_config is None:
        console.print("[red]No repo URL saved. Run `runongpu init` first.[/red]")
        return

    notebook_url = saved_config.get("notebook_url", "")
    
    console.print("[bold cyan]Starting RunOnGPU...[/bold cyan]")
    current_notebook_url = open_colab(notebook_url)
    
    save_notebook_url(current_notebook_url)
    
if __name__ == "__main__":
    app()
    