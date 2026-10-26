from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.routes.story_routes import router


ROOT = Path(__file__).resolve().parents[2]
STORAGE = ROOT / "storage"
VIDEOS = STORAGE / "videos"
VIDEOS.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="StoryWeave AI API",
    version="1.0.0",
    description="Narrative-to-animation generation API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/videos", StaticFiles(directory=VIDEOS), name="videos")
app.include_router(router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok", "service": "StoryWeave AI"}
