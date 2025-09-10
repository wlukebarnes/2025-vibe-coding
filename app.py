from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from dotenv import load_dotenv
from routers.todos import router as todos_router

# Load environment variables
load_dotenv()

app = FastAPI(title="2025 Vibe Coding Todo App")

# Mount static files directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Include routers
app.include_router(todos_router, prefix="/api", tags=["todos"])


@app.get("/")
async def read_root():
    """Serve the main index.html page"""
    try:
        return FileResponse("frontend/index.html", media_type="text/html")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error serving index page: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {"status": "healthy", "message": "App is running successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
