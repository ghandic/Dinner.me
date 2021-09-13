import logging
from dataclasses import dataclass
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient

from .models.dinnerme import DinnerMe, Card, Ingredient
from .models.dinnerly.menu_card import MenuCard

logger = logging.getLogger()


@dataclass
class MongoManager:
    client: AsyncIOMotorClient = None
    menu = None

    async def insert_recipe(self, recipe: DinnerMe) -> None:
        await self.menu["recipes"].replace_one({"id": recipe.id}, recipe.dict(), upsert=True)

    async def get_all_recipes(self) -> List[DinnerMe]:
        recipes = await self.menu["recipes"].find({}, {"_id": 0}).to_list(None)
        return [DinnerMe(**recipe) for recipe in recipes]

    async def get_recipe_by_id(self, id: int) -> Optional[DinnerMe]:
        recipe = await self.menu["recipes"].find_one({"id": id}, {"_id": 0})
        if recipe:
            return DinnerMe(**recipe)

    async def get_ingredients_by_id(self, id: int) -> Optional[Ingredient]:
        recipe = await self.menu["recipes"].find_one({"id": id}, {"_id": 0, "dinner_me_ingredients_standardized": 1})
        if recipe:
            return [Ingredient(**ingredient) for ingredient in recipe["dinner_me_ingredients_standardized"]]

    async def get_all_recipe_cards(self) -> List[Card]:
        recipes = (
            await self.menu["recipes"]
            .aggregate(
                [
                    {
                        "$project": {
                            "date": {"$dateFromString": {"dateString": "$startOfWeek"}},
                            "id": "$id",
                            "image": "$image",
                            "meal_type": "$meal_type",
                            "recipe_card_url": "$recipe_card_url",
                            "name": "$name",
                            "subtitle": "$subtitle",
                            "meal_attributes": "$meal_attributes",
                            "serves": "$serves",
                        }
                    },
                    {"$sort": {"date": -1}},
                ]
            )
            .to_list(None)
        )
        return [Card(**recipe) for recipe in recipes]

    async def recipe_exists(self, recipe: MenuCard) -> bool:
        return (
            await self.menu["recipes"].find_one({"name_with_subtitle": f"{recipe.title} {recipe.subtitle}"}) is not None
        )

