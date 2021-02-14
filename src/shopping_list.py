import json
from pathlib import Path

from tabulate import tabulate

from .conversion import Ingredient


class ShoppingList:
    def __init__(self) -> None:
        self.store = Path("data") / "dinnerly.json"
        with open(self.store, "r") as f:
            self.data = json.load(f)

    def create_list(self, ids):
        shopping_list = []
        meals = []
        for _id in ids:
            recipe = next(filter(lambda i: i["id"] == _id, self.data))
            meals.append({"name": recipe["name_with_subtitle"], "link": recipe["recipe_card_url"]})
            for standardized_ingredient in recipe["Dinner.me.ingredients.s"]:
                shopping_list.append(Ingredient(**standardized_ingredient))
        shopping_list_names = set(s.name for s in shopping_list)

        condensed_shopping_list = []
        for sln in shopping_list_names:
            condensed_shopping_list.append(sum(list(filter(lambda item: item.name == sln, shopping_list))))

        condensed_shopping_list.sort(key=lambda item: item.name)
        print("=" * 13)
        print("Meals")
        print("=" * 13)
        for meal in meals:
            print("-", meal["name"], meal["link"])

        print()

        print("=" * 13)
        print("Shopping List")
        print("=" * 13)
        print()

        print(
            tabulate(
                [item.to_dict() for item in condensed_shopping_list],
                headers={"name": "Name", "Amount": "amount", "Unit": "unit"},
            )
        )


if __name__ == "__main__":
    ShoppingList().create_list([65377, 65937])
