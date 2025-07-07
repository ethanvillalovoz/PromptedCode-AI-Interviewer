from src.app import app

# Entry point for running the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn

    # Start the FastAPI server on host 0.0.0.0 and port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)