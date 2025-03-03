from fastapi import FastAPI
from backend.routes.image_route import router as image_router
from backend.routes.camera_routes import router as camera_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

app.include_router(image_router)
app.include_router(camera_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


