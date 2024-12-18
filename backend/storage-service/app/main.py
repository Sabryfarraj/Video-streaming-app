from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from minio import Minio
from fastapi.responses import StreamingResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Minio(
    "minio:9000", access_key="minioadmin", secret_key="minioadmin", secure=False
)


@app.get("/stream/{video_path:path}")
async def stream_video(video_path: str):
    try:
        print(f"Attempting to stream: {video_path}")
        # Remove any 'videos/' prefix if it exists
        clean_path = video_path.replace("videos/", "")
        data = client.get_object(bucket_name="videos", object_name=clean_path)

        return StreamingResponse(
            data.stream(32 * 1024),
            media_type="video/mp4",
            headers={
                "Accept-Ranges": "bytes",
                "Content-Type": "video/mp4",
            },
        )
    except Exception as e:
        print(f"Error streaming video: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Error streaming video: {str(e)}")


@app.get("/health")
async def health_check():
    try:
        client.list_buckets()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
