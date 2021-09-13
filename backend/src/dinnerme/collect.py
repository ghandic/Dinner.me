import re
import json
from copy import deepcopy
from typing import List
import logging

import requests

from .models.dinnerly import WeeklyMenu, Recipe, GraqhQLResponse


logger = logging.getLogger()


class Collector:
    def __init__(self) -> None:
        api_token = re.findall('gon.api_token="(.*?)"', requests.get("https://dinnerly.com.au").text)[0]

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
            "authorization": f"Bearer {api_token}",
            "Origin": "https://dinnerly.com.au",
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "Trailers",
        }

    def get_menus(self, n_weeks: int) -> List[WeeklyMenu]:
        data = {
            "operationName": "GetMenu",
            "variables": {"imageSize": "MEDIUM", "numberOfWeeks": n_weeks},
            "query": """query GetMenu($numberOfWeeks: Int, $imageSize: ImageSizeEnum!) {
                menu(numberOfWeeks: $numberOfWeeks) {
                    startOfWeek
                    recipes {
                        id
                        slug
                        title
                        subtitle
                        mealType
                        category {
                            displayText
                            __typename
                        }
                        image(size: $imageSize) {
                            url
                            __typename
                        }
                        attributes {
                            key
                            __typename
                        }
                        __typename
                    }
                    __typename
                }
            }""",
        }
        response = requests.post("https://api.dinnerly.com/graphql", headers=self.headers, data=json.dumps(data))
        return GraqhQLResponse(**response.json()).data.menu

    def get_recipe(self, slug: str, id: int) -> Recipe:
        headers = deepcopy(self.headers)
        headers["Referer"] = f"https://dinnerly.com.au/menu{slug}/"
        response = requests.get(f"https://api.dinnerly.com/recipes/{id}", headers=headers, params=self.params)
        return Recipe(**response.json())

