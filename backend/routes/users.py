from fastapi import APIRouter, HTTPException, Body, Depends
from pydantic import BaseModel, EmailStr
from backend.db.connection import db
from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    token: str

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/api/auth/signup", response_model=UserOut)
async def signup(user: UserIn):
    existing = await db["users"].find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = pwd_context.hash(user.password)
    await db["users"].insert_one({"email": user.email, "password": hashed_pw})
    
    token = create_access_token({"sub": user.email})
    return {"email": user.email, "token": token}

@router.post("/api/auth/login", response_model=UserOut)
async def login(user: UserIn):
    found = await db["users"].find_one({"email": user.email})
    if not found or not pwd_context.verify(user.password, found["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": user.email})
    return {"email": user.email, "token": token}
