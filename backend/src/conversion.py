import re
import json
from pathlib import Path


u_replace = {
    "↉": "0",
    "⅟": "1",
    "⅒": ".1",
    "½": ".5",
    "⅓": ".333",
    "¼": ".25",
    "⅕": ".2",
    "⅙": ".16",
    "⅐": ".14",
    "⅛": ".125",
    "⅑": ".111",
    "⅔": ".666",
    "⅖": ".4",
    "¾": ".75",
    "⅗": ".6",
    "⅜": ".375",
    "⅘": ".8",
    "⅚": ".833",
    "⅝": ".625",
    "⅞": ".875",
}

unit_to_g = {"l": 1000, "tbsp": 17, "tbs": 17, "tsp": 5.69, "g": 1, "kg": 1000, "ml": 1}


class Ingredient:
    def __init__(self, amount, unit, name):
        self.amount = amount
        self.unit = unit if unit != "" else None
        self.name = name

    def standardize(self):
        if self.unit is None:
            return self

        mulitplier = unit_to_g[self.unit]
        return Ingredient(mulitplier * self.amount, "g", self.name)

    def __add__(self, other):
        if other == 0:
            return self
        if not isinstance(other, Ingredient):
            raise TypeError("Can only add ingredients")
        if (other.name != self.name) or (self.unit != other.unit):
            raise TypeError("Can only add same ingredients with same unit")
        return Ingredient(self.amount + other.amount, self.unit, self.name)

    __radd__ = __add__

    def __repr__(self) -> str:
        return f"Ingredient: '{self.name}', Amount: {self.amount}, Unit: {self.unit}"

    def to_dict(self):
        return {"name": self.name, "amount": self.amount, "unit": self.unit}


def structure_ingredient(ing_string):
    for u, r in u_replace.items():
        ing_string = ing_string.replace(u, r)
    # Getting multiplier, quantity, unit "2 x 400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce"
    quans = re.findall(f"(\d* x )?(\d*\.?\d+\s?)({'|'.join(unit_to_g.keys())})\s+", ing_string)
    if len(quans) == 0:
        quans_no_unit = re.findall("(\d* x )?\s?(\d*\.?\d+)\s", ing_string)
        if len(quans_no_unit) > 0:
            for q in quans_no_unit:
                quans.append((q[0], q[1], ""))
    if len(quans) == 0:
        return [Ingredient(1, "", ing_string)]

    # multiplier, quantity, unit -> quantity, unit, original
    tmp = []
    for q in quans:
        if q[0]:
            mq = float(q[0].strip(" x ")) * float(q[1])
        else:
            mq = float(q[1])
        tmp.append([mq, q[2], "".join(q)])

    # 400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce -> [(400, 'g', 'tomato paste, '), (295, 'ml', 'whole-egg mayonnaise and '), (500, 'ml', 'barbecue sauce')]
    tmp_name = ing_string
    output = []
    for t in reversed(tmp):
        ing_name = tmp_name[tmp_name.rfind(t[2]) + len(t[2]) :].strip().lower()
        ing_name = re.sub("\W$", "", ing_name)
        ing_name = re.sub(" and$", "", ing_name)
        output.append(Ingredient(t[0], t[1].strip(), ing_name))
        tmp_name = tmp_name[: tmp_name.rfind(t[2])]

    return output


class IngredientConverter:
    def __init__(self) -> None:
        self.store = Path("src/data") / "dinnerly.json"
        with open(self.store, "r") as f:
            self.data = json.load(f)

    def convert(self):
        for recipe in self.data:
            supplied, supplied_s, expected, expected_s = [], [], [], []
            for ing in recipe["ingredients"]:
                supplied += [e_ing.to_dict() for e_ing in structure_ingredient(ing["name"])]
                supplied_s += [e_ing.standardize().to_dict() for e_ing in structure_ingredient(ing["name"])]
            for ing in recipe["assumed_ingredients"]:
                expected += [e_ing.to_dict() for e_ing in structure_ingredient(ing["name"])]
                expected_s += [e_ing.standardize().to_dict() for e_ing in structure_ingredient(ing["name"])]

            recipe["Dinner.me.ingredients.s"] = supplied_s + expected_s
            recipe["Dinner.me.ingredients"] = supplied + expected
            # Kept in as a check but silly messages in here: {'name': 'a sense of culinary adventure'}
            # if not len(recipe["Dinner.me.ingredients.s"]) == len(recipe["assumed_ingredients"]) + len(
            #     recipe["ingredients"]
            # ):
            #     print(recipe["Dinner.me.ingredients.s"])
            #     print()
            #     print(recipe["assumed_ingredients"])
            #     print()
            #     print(recipe["ingredients"])

        with open(self.store, "w") as f:
            json.dump(self.data, f, indent=2)


if __name__ == "__main__":
    con = IngredientConverter()
    con.convert()
