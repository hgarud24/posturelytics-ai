import motor.motor_asyncio
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client["neuro_pose"]

async def connect_to_mongo():
    print("✅ Connected to MongoDB")
