from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from controller.item_controller import router as item_router
from controller.meal_controller import router as meal_router
from controller.meal_item_controller import router as meal_item_router
from controller.list_item_controller import router as list_item_router
from dao.list_item_dao import ListItemDao  # for fetching list items
from db import engine  # database engine to get connections

app = FastAPI()

# Enable CORS (allow all origins for development; adjust as needed in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all origins (or specify a list like ["http://localhost:8080"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory so '/static/*' paths serve files from the 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Jinja2 templates (assuming your HTML files are in a folder named 'templates')
templates = Jinja2Templates(directory="templates")

# Include API routers (you may optionally add a prefix like "/api" to avoid route conflicts)
app.include_router(item_router)   # e.g., GET/POST /items, etc.
app.include_router(meal_router)   # e.g., GET/POST /meals, etc.
app.include_router(meal_item_router)
app.include_router(list_item_router)  # includes GET/POST /list, etc.

@app.get("/main", response_class=HTMLResponse)
def render_main_page(request: Request):
    """Render the main page (main.html) with any required context data."""
    # The main page largely populates data via JS, so no extensive context needed.
    return templates.TemplateResponse("main.html", {"request": request})

@app.get("/main/list", response_class=HTMLResponse)
def render_list_page(request: Request):
    """Render the shopping list page (list.html) with current list items."""
    # Fetch the current list items from the database to pass into the template context
    with engine.connect() as conn:
        list_item_dao = ListItemDao(conn)
        current_items = list_item_dao.get_list_items()
    return templates.TemplateResponse("list.html", {"request": request, "items": current_items})

@app.get("/test", response_class=HTMLResponse)
def render_test_page(request: Request):
    """Render the test page (test.html)."""
    return templates.TemplateResponse("test.html", {"request": request})