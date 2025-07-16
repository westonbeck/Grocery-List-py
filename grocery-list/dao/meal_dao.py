from sqlalchemy import text
from sqlalchemy.engine import Connection
from models.meal import Meal

class MealDao:

    def __init__(self, conn: Connection):
        self.conn = conn

    def create_meal(self, name: str, description: str):
        self.conn.execute(text("insert into meal (name, description) values (:name, :description)"), {"name": name, "description": description})
        self.conn.commit()
    
    def get_all_meals(self) -> list[Meal]:
        result = self.conn.execute(text("select * from meal"))
        rows = result.mappings().all()
        return [Meal(meal_id=row["meal_id"], name=row["name"], description=row["description"])
                    for row in rows]
    
    def get_meal_by_id(self, meal_id: int) -> Meal | None:
        result = self.conn.execute(text("select * from meal where meal_id = :meal_id"), {"meal_id":meal_id}).mappings().fetchone()

        if result is None:
            return None

        return Meal(meal_id=result["meal_id"], name=result["name"], description=result["description"])
    
    def update_meal_by_id(self, meal_id: int, name: str, description: str):
        self.conn.execute(text("update meal set name = :name, description = :description where meal_id = :meal_id"), {"name":name, "description":description, "meal_id":meal_id})
        self.conn.commit()
    
    def delete_meal_by_id(self, meal_id: int):
        self.conn.execute(text("delete from meal where meal_id = :meal_id"), {"meal_id":meal_id})
        self.conn.commit()