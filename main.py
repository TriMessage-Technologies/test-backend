from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.api import router
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(router)

@app.get("/")
async def read_root():
    return FileResponse("frontend/index.html")

@app.get("/style.css")
async def serve_css():
    return FileResponse("frontend/style.css", media_type="text/css")

@app.get("/script.js")
async def serve_js():
    return FileResponse("frontend/script.js", media_type="application/javascript")

@app.get("/frontend/{path:path}")
async def serve_frontend(path: str):
    file_path = os.path.join("frontend", path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("frontend/index.html")
