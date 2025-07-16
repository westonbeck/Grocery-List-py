from fastapi import FastAPI
from controller.item_controller import router as item_router
from controller.meal_controller import router as meal_router
from controller.meal_item_controller import router as meal_item_router
from controller.list_item_controller import router as list_item_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello"}

app.include_router(item_router)
app.include_router(meal_router)
app.include_router(meal_item_router)
app.include_router(list_item_router)