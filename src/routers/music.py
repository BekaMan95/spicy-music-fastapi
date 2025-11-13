from fastapi import APIRouter, HTTPException, status, Header, Query, Depends, Request, Response
from src.config import db_dependency, get_db, SessionLocal

router = APIRouter(prefix="/api/music", tags=["music"])

@router.get("")
async def get_music_list():
    data = dict()

    return {
        "data": data,
        "message": "Here's the message!!",
        "success": True
    }
