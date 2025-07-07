from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.db import (
    get_challenge_quota,
    create_challenge,
    create_challenge_quota,
    reset_quota_if_needed,
    get_user_challenges
)
from ..utils import authenticate_and_get_user_details
from ..database.models import get_db
import json
from datetime import datetime

router = APIRouter()

class ChallengeRequest(BaseModel):
    difficulty: str

    class Config:
        json_schema_extra = {
            "example": {
                "difficulty": "easy"
            }
        }

@router.post("/generate-challenge")
async def generate_challenge(
    request: ChallengeRequest,
    db: Session = Depends(get_db)
):
    try:
        user_details = authenticate_and_get_user_details(request)
        user_id = user_details.get("user_id")
        
        quota = get_challenge_quota(db, user_id)
        if not quota:
            quota = create_challenge_quota(db, user_id)
        quota = reset_quota_if_needed(db, quota)

        if quota.quota_remaining <= 0:
            raise HTTPException(status_code=429, detail="Quota exhausted")
        
        challenge_data = None

        # TODO: generate challenge using LLM

        quota.quota_remaining -= 1
        db.commit()

        return challenge_data
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-history")
async def my_history(
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    challenges = get_user_challenges(db, user_id)
    return {"challenges": challenges}

@router.get("/quota")
async def get_quota(
    request: Request,
    db: Session = Depends(get_db)
):
    user_details = authenticate_and_get_user_details(request)
    user_id = user_details.get("user_id")

    quota = get_challenge_quota(db, user_id)
    if not quota:
        return {
            "user_id": user_id,
            "quota_remaining": 0,
            "last_reset_date": datetime.now()
        }
    
    quota = reset_quota_if_needed(db, quota)
    return quota