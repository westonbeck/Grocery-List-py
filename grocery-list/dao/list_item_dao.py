from sqlalchemy import text
from models.item import Item
from sqlalchemy.engine import Connection

class ListItemDao:

    def __init__(self, conn: Connection):
        self.conn = conn
    
    def create_list_item(self, item_id: int):
        self.conn.execute(text("insert into list_item (item_id) values (:item_id)"), {"item_id":item_id})
        self.conn.commit()
    
    def create_meal_list_items(self, meal_id: int):
        item_result = self.conn.execute(text("select * from item " \
        "where exists (select * from meal_item where meal_item.item_id = item.item_id and meal_item.meal_id = :meal_id)"), {"meal_id":meal_id})

        item_rows = item_result.mappings().all()

        for row in item_rows:
            self.conn.execute(text("insert into list_item (item_id) values (:item_id)"), {"item_id":row["item_id"]})

        self.conn.commit()

    def get_list_items(self) -> list[Item] | None:
        item_result = self.conn.execute(text("select * from item where exists (select * from list_item where list_item.item_id = item.item_id)"))
        item_rows = item_result.mappings().all()

        items = [Item(item_id=row["item_id"], name=row["name"], description=row["description"])
                for row in item_rows]

        return items
    
    def delete_list(self):
        self.conn.execute(text("delete from list_item"))
        self.conn.commit()
    
