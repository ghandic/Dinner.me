from typing import List

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from .dinnerly import Dinnerly
from .shopping_list import ShoppingList

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"],
)
dinner = Dinnerly()


@app.get("/recipes")
def menu():
    return dinner.recipes


@app.get("/report", response_class=HTMLResponse)
def shop(ids: List[int] = Query(None, description="List of names to greet")):
    shop = dinner.shop(ids)
    resp = ShoppingList.print_list(shop)
    return resp

