"""Main CLI application for the photo search tool."""

import typer
from rich.console import Console
from rich.progress import track
from rich.table import Table
from pathlib import Path

from src.photo_search.database import Database
from src.photo_search.photos_service import PhotosService
from src.photo_search.vllm_service import VLLMService

app = typer.Typer()
console = Console()


@app.command()
def index() -> None:
    """
    Index the photos in the Apple Photos library.

    This command fetches all photos, generates descriptions for them using the VLLM,
    and stores the information in the database.
    """
    console.print("Starting the indexing process...", style="bold green")
    db = Database()
    db.create_database()
    photos_service = PhotosService()
    vllm_service = VLLMService()

    try:
        photos = photos_service.get_photos()
        if not photos:
            console.print("No photos found in the library.", style="yellow")
            return

        console.print(f"Found {len(photos)} photos to process.")

        for photo in track(photos, description="Indexing photos..."):
            if not db.is_photo_indexed(photo.uuid):
                try:
                    description = vllm_service.get_description(Path(photo.path))
                    db.add_photo(photo, description)
                    console.print(f"Indexed photo [cyan]{photo.path}[/cyan].")
                except Exception as e:
                    console.print(f"Error processing photo {photo.path}: {e}", style="bold red")

    except FileNotFoundError:
        console.print("Could not find the Apple Photos library.", style="bold red")
    except Exception as e:
        console.print(f"An unexpected error occurred: {e}", style="bold red")

    console.print("Indexing process completed.", style="bold green")


@app.command()
def search(query: str) -> None:
    """
    Search for photos using a natural language query.

    Args:
        query: The search query.
    """
    console.print(f"Searching for photos matching: '[bold blue]{query}[/bold blue]'")
    db = Database()
    results = db.search_photos(query)

    if not results:
        console.print("No matching photos found.", style="yellow")
        return

    table = Table(title="Search Results")
    table.add_column("File Path", style="cyan")

    for path in results:
        table.add_row(path)

    console.print(table)


if __name__ == "__main__":
    app() 