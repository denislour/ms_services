import uvicorn
from enum import Enum
from typing import Optional

import typer
from rich import print
from rich.console import Console
from rich.table import Table

from core.app_factory import AppFactory

console = Console()
app = typer.Typer(
    help="Blog Service CLI",
    add_completion=False,
)

class Framework(str, Enum):
    FASTAPI = "fastapi"
    SANIC = "sanic"

class Database(str, Enum):
    SQLITE = "sqlite"
    MONGO = "mongo"

def run_app(
    framework: str,
    db: str,
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = False
):
    """Run the application with specified configuration"""
    web_app = AppFactory.create_app(framework=framework, db=db)
    
    if framework.lower() == 'fastapi':
        uvicorn.run(
            web_app,
            host=host,
            port=port,
            reload=reload
        )
    else:  # sanic
        web_app.run(
            host=host,
            port=port,
            debug=reload
        )

@app.command(name="run")
def run(
    framework: Framework = typer.Option(
        Framework.FASTAPI,
        "--framework", "-f",
        help="Web framework to use",
        case_sensitive=False,
    ),
    db: Database = typer.Option(
        Database.SQLITE,
        "--db", "-d",
        help="Database to use",
        case_sensitive=False,
    ),
    host: str = typer.Option(
        "0.0.0.0",
        "--host",
        help="Host to run the server on",
    ),
    port: int = typer.Option(
        8000,
        "--port", "-p",
        help="Port to run the server on",
    ),
    reload: bool = typer.Option(
        False,
        "--reload", "-r",
        help="Enable auto-reload for development",
    ),
):
    """Run the Blog Service with specified configuration"""
    # Show configuration table
    table = Table("Setting", "Value", title="Blog Service Configuration")
    table.add_row("Framework", framework.value)
    table.add_row("Database", db.value)
    table.add_row("Host", host)
    table.add_row("Port", str(port))
    table.add_row("Auto-reload", "✅" if reload else "❌")
    console.print(table)
    
    run_app(
        framework=framework.value,
        db=db.value,
        host=host,
        port=port,
        reload=reload,
    )

@app.command(name="dev")
def run_dev(
    framework: Framework = typer.Option(
        Framework.FASTAPI,
        "--framework", "-f",
        help="Web framework to use",
    ),
    db: Database = typer.Option(
        Database.SQLITE,
        "--db", "-d",
        help="Database to use",
    ),
):
    """Run in development mode with auto-reload enabled"""
    run(
        framework=framework,
        db=db,
        reload=True,
    )

if __name__ == "__main__":
    app()
