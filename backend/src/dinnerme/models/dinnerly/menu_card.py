from typing import List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    displayText: str
    __typename: str


class Image(BaseModel):
    url: Optional[str]
    __typename: str


class Attribute(BaseModel):
    key: str
    __typename: str


class MenuCard(BaseModel):
    id: int
    slug: str
    title: str
    subtitle: str
    mealType: str
    category: Category
    image: Image
    attributes: List[Attribute]
    __typename: str


class WeeklyMenu(BaseModel):
    startOfWeek: str
    recipes: List[MenuCard]


class Menus(BaseModel):
    menu: List[WeeklyMenu]


class GraqhQLResponse(BaseModel):
    data: Menus
