from typing import List, Optional

from pydantic import BaseModel


class Nutrition(BaseModel):
    calories: str
    carbs: str
    proteins: str
    fat: str


class Image(BaseModel):
    thumbnail: str
    small: Optional[str]
    medium: str
    large: Optional[str]


class Step(BaseModel):
    position: int
    title: str
    description: str
    photo: str


class Ingredient(BaseModel):
    name: str
    image: Image
    allergens: List[str]
    name_with_quantity: str


class AssumedIngredient(BaseModel):
    name: str


class AssumedCookingUtility(BaseModel):
    name: str


class Chef(BaseModel):
    name: str
    description: str
    bio: str
    image: Image
    slug: str


class Recipe(BaseModel):
    id: int
    name: str
    subtitle: str
    name_with_subtitle: str
    classic: bool
    slug: str
    variant_id: int
    country: str
    brand: str
    description: str
    meal_type: str
    calories: int
    difficulty: Optional[str]
    preparation_time: str
    product_type: str
    meal_attributes: List[str]
    nutrition: Nutrition
    sku: str
    recipe_card_url: str
    image: Image
    additional_allergens: List[str]
    steps: List[Step]
    ingredients: List[Ingredient]
    assumed_ingredients: List[AssumedIngredient]
    assumed_cooking_utilities: List[AssumedCookingUtility]
    chef: Chef
    cooking_tip: Optional[str]
    startOfWeek: Optional[str] = None
