from typing import List
from collections import Counter


from fastapi_utils.inferring_router import InferringRouter
from fastapi import Query
from tabulate import tabulate


from .shared import manager

router = InferringRouter()


@router.get("/recipes")
async def menu():
    return await manager.mongo.get_all_recipe_cards()


@router.get("/shopping_list")
async def shop(ids: List[int] = Query(None, description="List of ids to combine")):
    req = Counter(ids)
    shopping_list = []
    for id, qty in req.most_common():
        ingredients = await manager.mongo.get_ingredients_by_id(id)
        if ingredients:
            shopping_list += [i * qty for i in ingredients]

    shopping_list_names = {s.name for s in shopping_list}

    condensed_shopping_list = [
        sum(list(filter(lambda item: item.name == sln, shopping_list))) for sln in shopping_list_names
    ]

    condensed_shopping_list.sort(key=lambda item: item.name)
    return {
        "shopping_list": condensed_shopping_list,
        "tabulate": tabulate(
            [item.dict() for item in condensed_shopping_list],
            headers={"name": "Name", "Amount": "amount", "Unit": "unit"},
        ),
    }
