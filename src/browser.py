import json
from pathlib import Path

from jinja2 import Template


class MealBrowser:
    def __init__(self) -> None:
        self.template_folder = Path(__file__).parent / "assets" / "templates"
        self.store = Path("data") / "dinnerly.json"
        with open(self.store, "r") as f:
            self.data = json.load(f)

    def make_html(self):
        menu_template = Template(open(self.template_folder / "index.html").read())

        menu = [
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
            for recipe in self.data
        ]

        with open("demo.html", "w") as f:
            f.write(menu_template.render(menu=menu))
