from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine import Connection

from models.meal import Meal
from dao.meal_item_dao import MealItemDao
from db import engine

router = APIRouter()

def get_db():
    with engine.connect() as conn:
        yield conn

@router.get("/meals/{meal_id}/items")
def get_meal_items(meal_id: int, conn: Connection = Depends(get_db)) -> Meal:
    meal_item_dao = MealItemDao(conn)
    return meal_item_dao.get_meal_items_by_meal_id(meal_id)

@router.post("/meals/{meal_id}/items")
def create_meal_item(meal_id: int, item_id: int, conn: Connection = Depends(get_db)):
    meal_item_dao = MealItemDao(conn)
    meal_item_dao.create_meal_item(meal_id=meal_id, item_id=item_id)
    return Response(status_code=status.HTTP_200_OK)

@router.delete("/meals/{meal_id}/items/{item_id}")
def delete_meal_item(meal_id: int, item_id: int, conn: Connection = Depends(get_db)):
    meal_item_dao = MealItemDao(conn)
    meal_item_dao.delete_meal_item_by_ids(meal_id=meal_id, item_id=item_id)
    return Response(status_code=status.HTTP_200_OK)

@router.delete("/meals/{meal_id}/items")
def delete_all_meal_item(meal_id: int, conn: Connection = Depends(get_db)):
    meal_item_dao = MealItemDao(conn)
    meal_item_dao.delete_all_meal_items_by_meal_id(meal_id)
    return Response(status_code=status.HTTP_200_OK)