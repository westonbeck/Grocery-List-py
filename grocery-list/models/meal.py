from typing import Optional
from pydantic import BaseModel
from models.item import Item

class Meal(BaseModel):

    meal_id: int
    name: str
    description: str
    items: Optional[list[Item]] = None