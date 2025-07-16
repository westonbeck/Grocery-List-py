from sqlalchemy import text
from models.item import Item
from models.meal import Meal
from sqlalchemy.engine import Connection

class MealItemDao:

    def __init__(self, conn: Connection):
        self.conn = conn
    
    def create_meal_item(self, meal_id: int, item_id: int):
        self.conn.execute(text("insert into meal_item (meal_id, item_id) values (:meal_id, :item_id)"), {"meal_id":meal_id, "item_id":item_id})
        self.conn.commit()
    
    def get_meal_items_by_meal_id(self, meal_id: int) -> Meal | None:
        meal_result = self.conn.execute(text("select * from meal where meal_id = :meal_id"), {"meal_id":meal_id}).mappings().fetchone()
        item_result = self.conn.execute(text("select * from item " \
        "where exists (select * from meal_item " \
        "where meal_item.meal_id = :meal_id and meal_item.item_id = item.item_id)"), {"meal_id":meal_id})
        item_rows = item_result.mappings().all()

        items = [Item(item_id=row["item_id"], name=row["name"], description=row["description"])
                for row in item_rows]
        
        meal = Meal(meal_id=meal_id, name=meal_result["name"], description=meal_result["description"])

        meal.items = items

        return meal
    
    def delete_meal_item_by_ids(self, meal_id: int, item_id: int):
        self.conn.execute(text("delete from meal_item where meal_id = :meal_id and item_id = :item_id"), {"meal_id":meal_id, "item_id":item_id})
        self.conn.commit()
    
    def delete_all_meal_items_by_meal_id(self, meal_id: int):
        self.conn.execute(text("delete from meal_item where meal_id = :meal_id"), {"meal_id":meal_id})
    
