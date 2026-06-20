# Helps create terminal commands
import typer

#Helps print pretty terminal messages
from rich.console import Console

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

if __name__ == "__main__":
    app()