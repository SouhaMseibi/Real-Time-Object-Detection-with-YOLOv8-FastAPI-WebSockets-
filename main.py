import os
import argparse
import uvicorn
from fastapi import FastAPI
from backend.routes.image_route import router as image_router
from backend.routes.camera_routes import router as camera_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI()
# CAMERA_URL = os.getenv("CAMERA_URL", "0")

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

app.include_router(image_router)
app.include_router(camera_router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Start FastAPI server with optional camera URL.")
    parser.add_argument("-c", "--CAMERA_URL", type=str, default="0", help="Camera URL (default: local webcam)")
    
    args = parser.parse_args()
    print(f"Starting FastAPI server with CAMERA_URL: {args.CAMERA_URL}")

    # setting CAMERA_URL as an env variable so it can be accessed in camera_routes.py
    os.environ["CAMERA_URL"] = args.CAMERA_URL

    uvicorn.run(app, log_level="info" )