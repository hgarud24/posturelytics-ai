from fastapi import APIRouter, Body, Depends
from backend.db.connection import db 
from backend.utils.auth import get_current_user

router = APIRouter()

@router.post("/api/session")
async def save_session(data: dict = Body(...), user_email: str = Depends(get_current_user)):
    data["userId"] = user_email  
    result = await db["sessions"].insert_one(data)
    return {"message": "Session saved", "id": str(result.inserted_id)}
