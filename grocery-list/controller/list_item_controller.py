from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine import Connection

from models.item import Item
from dao.list_item_dao import ListItemDao
from db import engine

router = APIRouter()

def get_db():
    with engine.connect() as conn:
        yield conn

@router.get("/list")
def get_list_items(conn: Connection = Depends(get_db)) -> list[Item] | None:
    list_item_dao = ListItemDao(conn)
    return list_item_dao.get_list_items()

@router.post("/list/items")
def create_list_item(item_id: int, conn: Connection = Depends(get_db)):
    list_item_dao = ListItemDao(conn)
    list_item_dao.create_list_item(item_id=item_id)
    return Response(status_code=status.HTTP_200_OK)

@router.post("/list")
def create_list_meal_items(meal_id: int, conn: Connection = Depends(get_db)):
    list_item_dao = ListItemDao(conn)
    list_item_dao.create_meal_list_items(meal_id=meal_id)
    return Response(status_code=status.HTTP_200_OK)

@router.delete("/list")
def delete_list_items(conn: Connection = Depends(get_db)):
    list_item_dao = ListItemDao(conn)
    list_item_dao.delete_list()
    return Response(status_code=status.HTTP_200_OK)