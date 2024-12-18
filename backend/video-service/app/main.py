from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import get_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/videos")
async def get_videos(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, title, minio_location FROM videos")
    videos = cursor.fetchall()

    return [
        {"id": video[0], "title": video[1], "location": video[2]} for video in videos
    ]
