import json
from pathlib import Path

from tabulate import tabulate

from .conversion import Ingredient


class ShoppingList:
    def __init__(self, store) -> None:
        self.data = store

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
        return {"meals": meals, "shopping_list": condensed_shopping_list}

    @staticmethod
    def print_list(_list):
        underline = "=" * 13
        resp = [underline, "Meals", underline]
        unique_names = set()
        for meal in _list["meals"]:
            unique_names.add(f"- {meal['name']} {meal['link']}")
        resp = resp + list(unique_names)
        
        resp += [
            "",
            underline,
            "Shopping List",
            underline,
            "",
            tabulate(
                [item.to_dict() for item in _list["shopping_list"]],
                headers={"name": "Name", "Amount": "amount", "Unit": "unit"},
            ),
        ]

        return "\n".join(resp)


if __name__ == "__main__":
    ShoppingList().create_list([65377, 65937])
