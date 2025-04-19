from fastapi import APIRouter, Body, Depends
from backend.db.connection import db 
from backend.utils.auth import get_current_user
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import openai


load_dotenv()
print("Loaded API key:", os.getenv("OPENAI_KEY"))

# openai.api_key=os.getenv("OPENAI_KEY")

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_KEY"))

async def generate_gpt_feedback(session):
    logs = session.get("logs", [])
    focus = [l.get("attention") for l in logs]
    posture = [l.get("posture") for l in logs]

    focus_score = focus.count("focused") / len(focus) if focus else 0
    posture_score = posture.count("good") / len(posture) if posture else 0
    zoneouts = focus.count("distracted")
    slouch_time = posture.count("slouching")

    prompt = (
        f"Summarize this productivity session:\n"
        f"- Focus Score: {focus_score:.2f}\n"
        f"- Posture Score: {posture_score:.2f}\n"
        f"- Zoneouts: {zoneouts}\n"
        f"- Slouching Entries: {slouch_time}\n"
        f"Give practical tips for improvement."
    )

    try:
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return "Could not generate feedback."


router = APIRouter()

@router.post("/api/session")
async def save_session(data: dict = Body(...), user_email: str = Depends(get_current_user)):
    data["userId"] = user_email

    feedback = await generate_gpt_feedback(data)
    data["gpt_feedback"] = feedback

    result = await db["sessions"].insert_one(data)
    return {
        "message": "Session saved",
        "id": str(result.inserted_id),
        "feedback": feedback
    }
