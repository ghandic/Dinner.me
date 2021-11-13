import re
from typing import List, Optional

from pydantic import BaseModel

from ..dinnerly.recipe import Recipe

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
    # Junk
    "(optional)": "",
    "(APPROVED BY RS)": "",
    "(MAX ALLOWED FOR LC)": "",
    "(APPROVED BY YN)": "",
    ", plus extra for greasing": "",
}

unit_to_g = {"l": 1000, "tbsp": 17, "tbs": 17, "tsp": 5.69, "g": 1, "kg": 1000, "ml": 1, "cup": 250, "cups": 250}
blacklist_ingredients = ["boiling water", "plate for serving"]
force_ingredients = {
    "wine vinegar": "red/white/balsamic vinegar",
    # multiples
    "small garlic clove": "garlic clove",
    "garlic cloves": "garlic clove",
    "eggs": "egg",
    "tomatoes": "tomato",
}


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str

    def standardize(self) -> "Ingredient":
        if not self.unit:
            return self

        multiplier = unit_to_g[self.unit]
        return Ingredient(amount=multiplier * self.amount, unit="g", name=self.name)

    def __mul__(self, other: float) -> "Ingredient":
        if not isinstance(other, (float, int)):
            raise TypeError("Can only multiply ingredient by number")
        return Ingredient(amount=self.amount * other, unit=self.unit, name=self.name)

    def __add__(self, other: "Ingredient") -> "Ingredient":
        if other == 0:
            return self
        if not isinstance(other, Ingredient):
            raise TypeError("Can only add ingredients")
        if (other.name != self.name) or (self.unit != other.unit):
            raise TypeError(f"Can only add same ingredients with same name and unit, Unit: {self.unit} vs {other.unit}, Name: {self.name} vs {other.name}")
        return Ingredient(amount=self.amount + other.amount, unit=self.unit, name=self.name)

    __radd__ = __add__
    __rmul__ = __mul__


def structure_ingredient(value: str) -> List[Ingredient]:
    for u, r in u_replace.items():
        value = value.replace(u, r)

    value = value.strip()
    optional = "\)?"
    # Getting multiplier, quantity, unit "2 x 400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce"
    quans = re.findall(f"(\d* x )?(\d*\.?\d+\s?)({f'{optional}|'.join(unit_to_g.keys())}{optional})\s+", value)
    if len(quans) == 0:
        quans_no_unit = re.findall("(\d* x )?\s?(\d*\.?\d+)\s", value)
        if len(quans_no_unit) > 0:
            for q in quans_no_unit:
                quans.append((q[0], q[1], ""))
    if len(quans) == 0:
        if not any(blacklist_item in value for blacklist_item in blacklist_ingredients):
            value = re.sub("^can ", "", value)
            for force_ing, replacement in force_ingredients.items():
                if force_ing in value:
                    value = replacement
                    break
            return [Ingredient(amount=1, unit="", name=value.strip())]

    # multiplier, quantity, unit -> quantity, unit, original
    tmp = []
    for q in quans:
        if q[0]:
            mq = float(q[0].strip(" x ")) * float(q[1])
        else:
            mq = float(q[1])
        tmp.append([mq, q[2], "".join(q)])

    # 400g tomato paste, 295ml whole-egg mayonnaise and 500ml barbecue sauce -> [(400, 'g', 'tomato paste, '), (295, 'ml', 'whole-egg mayonnaise and '), (500, 'ml', 'barbecue sauce')]
    tmp_name = value
    output = []
    for t in reversed(tmp):
        ing_name = tmp_name[tmp_name.rfind(t[2]) + len(t[2]) :].strip().lower()
        ing_name = re.sub("\W$", "", ing_name)
        ing_name = re.sub(" and$", "", ing_name)
        ing_name = re.sub("^can ", "", ing_name)
        if not any(blacklist_item in ing_name for blacklist_item in blacklist_ingredients):
            for force_ing, replacement in force_ingredients.items():
                if force_ing in ing_name:
                    ing_name = replacement
                    break
            output.append(Ingredient(amount=t[0], unit=t[1].strip().strip(")"), name=ing_name.strip()))
        tmp_name = tmp_name[: tmp_name.rfind(t[2])]

    return output


def parse_ingredients(ingredients: "Item") -> List[Ingredient]:
    structured_ingredients = []
    for ingredient_value in ingredients:
        for structured_ingredient in structure_ingredient(ingredient_value.name):
            structured_ingredients.append(structured_ingredient)
    return structured_ingredients


class DinnerMe(Recipe):
    dinner_me_ingredients: Optional[List[Ingredient]] = []
    dinner_me_ingredients_standardized: Optional[List[Ingredient]] = []
    serves: Optional[int] = 2

    def set_ingredients(self):
        self.dinner_me_ingredients = parse_ingredients(self.ingredients) + parse_ingredients(self.assumed_ingredients)
        self.dinner_me_ingredients_standardized = [i.standardize() for i in self.dinner_me_ingredients]

    def set_servings(self):
        if "feed-a-crowd" in self.slug:
            self.serves = 4
