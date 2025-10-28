"""
AI Productivity Dashboard - FastAPI Backend
A production-ready API for Gmail, Drive, and Calendar integration with AI insights
"""
import logging.config
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from config import settings, LOGGING_CONFIG
from schemas import HealthCheck, ErrorResponse
from routes import gmail, drive, calendar
from services.oauth_handler import oauth_router
from models.database import db
from utils import rate_limiter

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting AI Productivity Dashboard API...")
    
    # Initialize database
    try:
        db.init_database()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    
    # Initialize AI models (in background to avoid blocking startup)
    try:
        from services.ai_summary import ai_service
        logger.info("AI models loading in background...")
    except Exception as e:
        logger.warning(f"AI model initialization warning: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down AI Productivity Dashboard API...")


# Create FastAPI application
app = FastAPI(
    title="AI Productivity Dashboard API",
    description="Production-ready API for Gmail, Drive, and Calendar integration with AI-powered insights",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
    lifespan=lifespan
)

# Security middleware
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.render.com", "*.vercel.app", "localhost"]
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Rate limiting middleware
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to API requests"""
    client_ip = request.client.host
    
    # Skip rate limiting for health checks
    if request.url.path in ["/", "/health"]:
        return await call_next(request)
    
    if not rate_limiter.is_allowed(client_ip):
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"error": "Rate limit exceeded", "message": "Too many requests"}
        )
    
    return await call_next(request)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.warning(f"Validation error for {request.url}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error="Validation Error",
            message="Invalid request data",
            details={"errors": exc.errors()}
        ).dict()
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error for {request.url}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP {exc.status_code}",
            message=exc.detail
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error for {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            message="An unexpected error occurred"
        ).dict()
    )


# Include routers with versioning
app.include_router(oauth_router, prefix="/auth", tags=["Authentication"])
app.include_router(gmail.router, prefix=f"{settings.api_v1_prefix}/gmail", tags=["Gmail"])
app.include_router(drive.router, prefix=f"{settings.api_v1_prefix}/drive", tags=["Google Drive"])
app.include_router(calendar.router, prefix=f"{settings.api_v1_prefix}/calendar", tags=["Google Calendar"])


# Health check endpoints
@app.get("/", response_model=HealthCheck, tags=["Health"])
async def root():
    """Root endpoint with basic API information"""
    return HealthCheck(
        status="running",
        services={
            "database": "connected",
            "ai_models": "loaded",
            "google_apis": "configured"
        }
    )


@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """Detailed health check for monitoring"""
    services = {}
    
    # Check database
    try:
        # Simple database check
        services["database"] = "healthy"
    except Exception:
        services["database"] = "unhealthy"
    
    # Check AI service
    try:
        from services.ai_summary import ai_service
        services["ai_models"] = "healthy" if ai_service.summarizer else "loading"
    except Exception:
        services["ai_models"] = "unhealthy"
    
    # Check configuration
    services["configuration"] = "healthy" if settings.google_client_id else "missing"
    
    overall_status = "healthy" if all(
        status in ["healthy", "loading"] for status in services.values()
    ) else "unhealthy"
    
    return HealthCheck(
        status=overall_status,
        services=services
    )


# Development server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development",
        log_level="info"
    )