from fastapi import APIRouter, Body
from backend.db.connection import db  # your MongoDB instance

router = APIRouter()

@router.post("/api/session")
async def save_session(data: dict = Body(...)):
    await db["sessions"].insert_one(data)
    return {"message": "Session saved successfully"}
