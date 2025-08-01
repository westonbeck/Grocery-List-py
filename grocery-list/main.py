from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from controller.item_controller import router as item_router
from controller.meal_controller import router as meal_router
from controller.meal_item_controller import router as meal_item_router
from controller.list_item_controller import router as list_item_router

app = FastAPI()

# Configure CORS to allow frontend JS to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, DELETE, etc.)
    allow_headers=["*"]   # Allow all headers
)

# Mount the static directory to serve static files (JS, CSS, HTML, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Serve the main HTML page at the root URL
@app.get("/")
def read_index():
    return FileResponse("static/index.html")  # Serves index.html on accessing '/'

@app.get("/main")
async def main_view(request: Request):
    # fetch or compute the context your JSP expected
    items = items_db
    return templates.TemplateResponse("main.html", {"request": request, "items": items})

@app.get("/test")
async def test_view(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/list")
async def list_view(request: Request):
    current = current_list
    return templates.TemplateResponse("list.html", {
        "request": request,
        "list_items": current
    })

app.include_router(item_router)
app.include_router(meal_router)
app.include_router(meal_item_router)
app.include_router(list_item_router)