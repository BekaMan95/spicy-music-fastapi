from fastapi import FastAPI
from src.config import engine, Base
from src.routers import user_router, music_router


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(music_router)

@app.get("/api/test")
async def test():
    return {
        "message": "Hello FastAPI!!",
        "success": True
    }


