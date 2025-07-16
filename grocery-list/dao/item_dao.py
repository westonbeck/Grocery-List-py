from sqlalchemy import text
from sqlalchemy.engine import Connection
from models.item import Item

class ItemDao:
    
    def __init__(self, conn: Connection):
        self.conn = conn

    def create_item(self, name: str, description: str):
        self.conn.execute(text("insert into item (name, description) values (:name, :description)"), {"name": name, "description": description})
        self.conn.commit()

    def get_all_items(self) -> list[Item]:
        result = self.conn.execute(text("select * from item"))
        rows = result.mappings().all()
        return [Item(item_id=row["item_id"], name=row["name"], description=row["description"])
                for row in rows]
    
    def get_item_by_id(self, item_id: int) -> Item | None:
        result = self.conn.execute(text("select * from item where item.item_id = :id"), {"id": item_id}).mappings().fetchone()

        if result is None:
            return None
            
        return Item(item_id=result["item_id"], name=result["name"], description=result["description"])
    
    def update_item_by_id(self, item_id: int, name: str, description: str):
        self.conn.execute(text("update item set name = :name, description = :description where item_id = :id"), {"id": item_id, "name": name, "description": description})
        self.conn.commit()
    
    def delete_item_by_id(self, item_id: int):
        self.conn.execute(text("delete from item where item_id = :id"), {"id": item_id})
        self.conn.commit()