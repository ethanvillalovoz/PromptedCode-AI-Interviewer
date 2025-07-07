from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .routes import challenge, webhooks

# Create the FastAPI application instance
app = FastAPI()

# Add CORS middleware to allow cross-origin requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (for development; restrict in production)
    allow_credentials=True,     # Allow cookies and authentication headers
    allow_methods=["*"],        # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],        # Allow all headers
)

# Include the challenge-related API routes under the /api prefix
app.include_router(challenge.router, prefix="/api")

# Include the webhook-related API routes under the /webhooks prefix
app.include_router(webhooks.router, prefix="/webhooks")