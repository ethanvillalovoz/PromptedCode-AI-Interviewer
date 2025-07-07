from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Clerk SDK with the API key from environment variables
clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_API_KEY"))

def authenticate_and_get_user_details(request):
    """
    Authenticate the incoming request using Clerk and return user details.
    Raises HTTPException if authentication fails.
    """
    try:
        # Authenticate the request using Clerk SDK
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=[
                    "http://localhost:5173",
                    "http://localhost:5174"
                ],
                jwt_key=os.getenv("JWT_KEY")
            )
        )
        # If the user is not signed in, raise an unauthorized error
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Extract the user ID from the token payload
        user_id = request_state.payload.get("sub")

        # Return the user ID in a dictionary
        return {
            "user_id": user_id
        }
    except Exception as e:
        # Raise a 500 error if authentication fails for any reason
        raise HTTPException(status_code=500, detail="Invalid credentials")