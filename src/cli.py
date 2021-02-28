from typing import List

import typer

from .download import DinnerlyDownloader
from .conversion import IngredientConverter
from .shopping_list import ShoppingList
from .browser import MealBrowser

app = typer.Typer()


@app.command()
def download():
    down = DinnerlyDownloader()
    down.download_recipes()
    down.download_images()
    IngredientConverter().convert()


@app.command()
def shop(ids: List[int]):
    ShoppingList().create_list(ids)


@app.command()
def browse():
    MealBrowser().make_html()


if __name__ == "__main__":
    app()
