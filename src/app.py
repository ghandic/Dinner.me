from typing import List
from pathlib import Path

from fastapi import Request, FastAPI, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from dinnerly import Dinnerly
from shopping_list import ShoppingList

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"],
)
dinner = Dinnerly()

assets = Path(__file__).parent / "assets"
data = Path(__file__).parent / "data"
app.mount("/assets", StaticFiles(directory=assets), name="assets")
app.mount("/data", StaticFiles(directory=data), name="data")
templates = Jinja2Templates(directory=assets / "templates")


@app.get("/", response_class=HTMLResponse)
def menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request, "menu": dinner.menu})


@app.get("/report", response_class=HTMLResponse)
def shop(request: Request, ids: List[int] = Query(None, description="List of names to greet")):
    shop = dinner.shop(ids)
    ShoppingList.print_list(shop)
    return templates.TemplateResponse("shopping.html", {"request": request, "shop": shop})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", port=5555, host="0.0.0.0", reload=True)
