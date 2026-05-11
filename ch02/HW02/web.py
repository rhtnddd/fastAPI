from fastapi import FastAPI
from typing import Optional
from model import LostItem
import data


app = FastAPI()


@app.get("/lost-items")
def get_lost_items(returned: Optional[bool] = None, place: Optional[str] = None) -> list[LostItem]:
    if returned is None and place is None:
        return data.get_items()
    return data.filter_items(returned, place)


@app.get("/lost-items/{item_id}")
def get_lost_item(item_id: int) -> LostItem | dict:
    item = data.get_item_by_id(item_id)

    if item is None:
        return {"error": "not found"}

    return item