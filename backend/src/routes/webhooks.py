from fastapi import APIRouter, Request, HTTPException, Depends
from ..database.db import create_challenge_quota
from ..database.models import get_db
from svix.webhooks import Webhook
import os
import json

router = APIRouter()

@router.post("/clerk")
async def handle_user_created(
    request: Request,
    db=Depends(get_db)
):
    """
    Endpoint to handle Clerk webhook events for user creation.
    When a new user is created in Clerk, this endpoint is called to
    create a corresponding challenge quota record in the database.
    """
    # Get the Clerk webhook secret from environment variables
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")

    if not webhook_secret:
        # If the secret is not set, return a server error
        raise HTTPException(
            status_code=500,
            detail="CLERK_WEBHOOK_SECRET not set"
        )

    # Read the raw request body and headers
    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)

    try:
        # Verify the webhook signature using svix
        wh = Webhook(webhook_secret)
        wh.verify(payload, headers)

        # Parse the webhook payload as JSON
        data = json.loads(payload)

        # Only handle 'user.created' events
        if data.get("type") != "user.created":
            return {"status": "ignored"}

        # Extract user data and user ID from the payload
        user_data = data.get("data", {})
        user_id = user_data.get("id")

        # Create a challenge quota record for the new user
        create_challenge_quota(db, user_id)

        return {"status": "success"}
    except Exception as e:
        # If verification fails or any error occurs, return unauthorized
        raise HTTPException(status_code=401, detail=str(e))