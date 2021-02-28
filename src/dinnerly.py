import json
from pathlib import Path

from download import DinnerlyDownloader
from conversion import IngredientConverter
from shopping_list import ShoppingList


class Dinnerly:
    def __init__(self) -> None:
        self.data_store = Path("data")
        self.dinnerly_cache = self.data_store / "dinnerly.json"
        self.sync()

    def load_recipes(self):
        with open(self.dinnerly_cache, "r") as f:
            self.recipes = json.load(f)

    def sync(self):
        down = DinnerlyDownloader()
        down.download_recipes()
        down.download_images()
        IngredientConverter().convert()
        self.load_recipes()

    @property
    def menu(self):
        return [
            {
                "id": recipe["id"],
                "name": recipe["name"],
                "subtitle": recipe["subtitle"],
                "meal_type": recipe["meal_type"],
                "title": recipe["name"],
                "labels": [{"name": l, "link": l} for l in recipe["meal_attributes"]],
                "image": recipe["Dinner.me.image"],
                "link": recipe["Dinner.me.instructions"],
            }
            for recipe in self.recipes
        ]

    def shop(self, ids):
        return ShoppingList(self.recipes).create_list(ids)

