from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.meal import Meal
from models.item import Item

class MealItem(Base):
    __tablename__ = "meal_item"

    meal_item_id = Column("meal_item_id", Integer, primary_key=True)
    meal_id = Column(Integer, ForeignKey("meal.meal_id"))
    item_id = Column(Integer, ForeignKey("item.item_id"))

    meal = relationship(Meal, back_populates="meal_items")
    item = relationship(Item, back_populates="meal_items")