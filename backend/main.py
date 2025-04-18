from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db.connection import connect_to_mongo
from backend.routes.session import router as session_router 
from backend.routes.users import router as user_router


app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # update in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)

@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

app.include_router(session_router)

@app.get("/")
def home():
    return {"message": "Posturelytics.AI Backend is running "}
