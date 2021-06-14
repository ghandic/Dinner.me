import re
import asyncio
import aiohttp
import json
import requests
import shutil
from pathlib import Path
import logging
import sys
from copy import deepcopy

import nest_asyncio

nest_asyncio.apply()
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger()


class DinnerlyDownloader:
    def __init__(self) -> None:
        self.data_store = Path("src/data")
        self.dinnerly_cache = self.data_store / "dinnerly.json"
        if not self.dinnerly_cache.exists():
            with open(self.dinnerly_cache, "w") as f:
                json.dump([], f)

        if not (self.data_store / "images").exists():
            (self.data_store / "images").mkdir()
        if not (self.data_store / "instructions").exists():
            (self.data_store / "instructions").mkdir()
        self.api_token = re.findall('gon.api_token="(.*?)"', requests.get("https://dinnerly.com.au").text)[0]

        self.params = (
            ("brand", "dn"),
            ("country", "au"),
            ("product_type", "web"),
        )

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Accept": "*/*",
            "Accept-Language": "en-GB,en;q=0.5",
            "Referer": "https://dinnerly.com.au/menu",
            "content-type": "application/json",
            "authorization": f"Bearer {self.api_token}",
            "Origin": "https://dinnerly.com.au",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "Trailers",
        }

    def download_images(self):
        with open(self.dinnerly_cache, "r") as f:
            recipes = json.load(f)

        for recipe in recipes:
            if recipe.get("Dinner.me.image") is None:
                logger.info(f"Fetching image for recipe id: {recipe['id']}")
                response = requests.get(recipe["image"]["medium"], stream=True)
                response.raw.decode_content = True
                img_path = self.data_store / "images" / f'{recipe["id"]}.jpg'
                with open(img_path, "wb") as f:
                    shutil.copyfileobj(response.raw, f)
                recipe["Dinner.me.image"] = str(img_path).strip("/src")
            else:
                logger.info(f"Using cached image for recipe id: {recipe['id']}")

            if recipe.get("Dinner.me.instructions") is None:
                logger.info(f"Fetching instructions for recipe id: {recipe['id']}")
                response = requests.get(recipe["recipe_card_url"], stream=True)
                response.raw.decode_content = True
                pdf_path = self.data_store / "instructions" / f'{recipe["id"]}.pdf'
                with open(pdf_path, "wb") as f:
                    shutil.copyfileobj(response.raw, f)
                recipe["Dinner.me.instructions"] = str(pdf_path).strip("/src")
            else:
                logger.info(f"Using cached instructions for recipe id: {recipe['id']}")

        with open(self.dinnerly_cache, "w") as f:
            json.dump(recipes, f, indent=2)

    async def download_async_recipes(self, requests):
        recipes = []
        async with aiohttp.ClientSession() as session:
            for request in requests:
                logger.info(f"Fetching recipe for id: {request['id']}")
                async with session.get(**request["request"]) as resp:
                    recipe = await resp.json()
                    recipes.append(recipe)
        return recipes

    def download_recipes(self):
        data = '{"operationName":"GetMenu_Web","variables":{"imageSize":"MEDIUM"},"query":"query GetMenu_Web($numberOfWeeks: Int, $imageSize: ImageSizeEnum!) {\\n menu(numberOfWeeks: $numberOfWeeks) {\\n startOfWeek\\n recipes {\\n id\\n slug\\n title\\n subtitle\\n mealType\\n category {\\n displayText\\n __typename\\n }\\n image(size: $imageSize) {\\n url\\n __typename\\n }\\n attributes {\\n key\\n __typename\\n }\\n __typename\\n }\\n __typename\\n }\\n}\\n"}'

        response = requests.post("https://api.dinnerly.com/graphql", headers=self.headers, data=data)
        data = response.json()

        with open(self.dinnerly_cache, "r") as f:
            recipes = json.load(f)

        current_ids = [r["id"] for r in recipes]
        to_download = []
        for week in data["data"]["menu"]:
            for recipe in week["recipes"]:
                if not recipe["id"] in current_ids:
                    headers = deepcopy(self.headers)
                    headers["Referer"] = f'https://dinnerly.com.au/menu{recipe["slug"]}/'
                    to_download.append(
                        {
                            "id": recipe["id"],
                            "request": {
                                "url": f'https://api.dinnerly.com/recipes/{recipe["id"]}',
                                "headers": headers,
                                "params": self.params,
                            },
                        }
                    )
                else:
                    logger.info(f"Using cached recipe for id: {recipe['id']}")

        loop = asyncio.get_event_loop()
        new_recipes = loop.run_until_complete(self.download_async_recipes(to_download))
        recipes += new_recipes

        with open(self.dinnerly_cache, "w") as f:
            json.dump(recipes, f, indent=2)
