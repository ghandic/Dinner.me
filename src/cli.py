from typing import List

import typer

from .download import DinnerlyDownloader
from .conversion import IngredientConverter
from .shopping_list import ShoppingList

app = typer.Typer()


@app.command()
def download():
    DinnerlyDownloader().download_recipes()
    IngredientConverter().convert()


@app.command()
def shop(ids: List[int]):
    ShoppingList().create_list(ids)


if __name__ == "__main__":
    app()
