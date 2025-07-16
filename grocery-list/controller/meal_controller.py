from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine import Connection

from models.meal import Meal
from dao.meal_dao import MealDao
from db import engine

router = APIRouter()

def get_db():
    with engine.connect() as conn:
        yield conn

@router.get("/meals")
def get_all_meals(conn: Connection = Depends(get_db)) -> list[Meal]:
    meal_dao = MealDao(conn)
    return meal_dao.get_all_meals()

@router.get("/meals/{id}")
def get_meal(id: int, conn: Connection = Depends(get_db)) -> Meal | None:
    meal_dao = MealDao(conn)
    return meal_dao.get_meal_by_id(id)

@router.post("/meals")
def create_meal(name: str, description: str, conn: Connection = Depends(get_db)):
    meal_dao = MealDao(conn)
    meal_dao.create_meal(name, description)
    return Response(status_code=status.HTTP_200_OK)

@router.post("/meals/{id}")
def update_meal(id: int, name: str, description: str, conn: Connection = Depends(get_db)):
    meal_dao = MealDao(conn)
    meal_dao.update_meal_by_id(id, name, description)
    return Response(status_code=status.HTTP_200_OK)

@router.delete("/meals/{id}")
def delete_meal(id: int, conn: Connection = Depends(get_db)):
    meal_dao = MealDao(conn)
    meal_dao.delete_meal_by_id(id)
    return Response(status_code=status.HTTP_200_OK)