from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.engine import Connection

from models.item import Item
from dao.item_dao import ItemDao
from db import engine

router = APIRouter()

def get_db():
    with engine.connect() as conn:
        yield conn

@router.get("/items")
def get_all_items(conn: Connection = Depends(get_db)) -> list[Item]:
    item_dao = ItemDao(conn)
    return item_dao.get_all_items()

@router.get("/items/{id}")
def get_item(id: int, conn: Connection = Depends(get_db)) -> Item | None:
    item_dao = ItemDao(conn)
    return item_dao.get_item_by_id(id)

@router.post("/items")
def create_item(name: str, description: str, conn: Connection = Depends(get_db)):
    item_dao = ItemDao(conn)
    item_dao.create_item(name, description)
    return Response(status_code=status.HTTP_200_OK)

@router.post("/items/{id}")
def update_item(id: int, name: str, description: str, conn: Connection = Depends(get_db)):
    item_dao = ItemDao(conn)
    item_dao.update_item_by_id(id, name, description)
    return Response(status_code=status.HTTP_200_OK)

@router.delete("/items/{id}")
def delete_item(id: int, conn: Connection = Depends(get_db)):
    item_dao = ItemDao(conn)
    item_dao.delete_item_by_id(id)
    return Response(status_code=status.HTTP_200_OK)