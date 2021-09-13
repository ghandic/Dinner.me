from typing import List, Optional

from pydantic import BaseModel


class Image(BaseModel):
    thumbnail: str
    small: Optional[str]
    medium: str
    large: Optional[str]


class Card(BaseModel):

    id: int
    image: Image
    meal_type: str
    recipe_card_url: str
    name: str
    subtitle: str
    meal_attributes: List[str]
    serves: int

