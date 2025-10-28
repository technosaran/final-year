from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from routes import gmail, drive, calendar
from services.oauth_handler import oauth_router

app = FastAPI(
    title="AI Productivity Dashboard API",
    description="Backend API for productivity insights from Gmail, Drive, and Calendar",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(oauth_router, prefix="/auth", tags=["authentication"])
app.include_router(gmail.router, prefix="/api/gmail", tags=["gmail"])
app.include_router(drive.router, prefix="/api/drive", tags=["drive"])
app.include_router(calendar.router, prefix="/api/calendar", tags=["calendar"])

@app.get("/")
async def root():
    return {"message": "AI Productivity Dashboard API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-productivity-dashboard"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)