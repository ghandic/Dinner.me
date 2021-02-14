import re
import json
import requests
from pathlib import Path


class DinnerlyDownloader:
    def __init__(self) -> None:
        self.store = Path("data") / "dinnerly.json"
        if not self.store.exists():
            with open(self.store, "w") as f:
                json.dump([], f)
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

    def download_recipes(self):
        data = '{"operationName":"GetMenu_Web","variables":{"imageSize":"MEDIUM"},"query":"query GetMenu_Web($numberOfWeeks: Int, $imageSize: ImageSizeEnum!) {\\n menu(numberOfWeeks: $numberOfWeeks) {\\n startOfWeek\\n recipes {\\n id\\n slug\\n title\\n subtitle\\n mealType\\n category {\\n displayText\\n __typename\\n }\\n image(size: $imageSize) {\\n url\\n __typename\\n }\\n attributes {\\n key\\n __typename\\n }\\n __typename\\n }\\n __typename\\n }\\n}\\n"}'

        response = requests.post("https://api.dinnerly.com/graphql", headers=self.headers, data=data)
        data = response.json()

        with open(self.store, "r") as f:
            recipes = json.load(f)

        current_ids = [r["id"] for r in recipes]

        for week in data["data"]["menu"]:
            for recipe in week["recipes"]:
                if not recipe["id"] in current_ids:
                    print(f"Fetching recipe for id: {recipe['id']}")
                    self.headers["Referer"] = f'https://dinnerly.com.au/menu{recipe["slug"]}/'
                    response = requests.get(
                        f'https://api.dinnerly.com/recipes/{recipe["id"]}', headers=self.headers, params=self.params
                    )
                    recipes.append(response.json())
                else:
                    print(f"Using cached recipe for id: {recipe['id']}")

        with open(self.store, "w") as f:
            json.dump(recipes, f, indent=2)
