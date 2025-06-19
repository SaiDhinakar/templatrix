from fastapi import APIRouter, Depends
from utils.database import health_check_database
from utils.responses import create_response
from utils.config import get_settings, Settings

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check(settings: Settings = Depends(get_settings)):
    """General health check endpoint"""
    db_healthy = health_check_database()
    
    return create_response(
        message="Service is healthy" if db_healthy else "Service has issues",
        data={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "database": "healthy" if db_healthy else "unhealthy",
            "debug_mode": settings.debug
        },
        success=db_healthy
    )

@router.get("/database")
def database_health():
    """Database-specific health check"""
    db_healthy = health_check_database()
    
    return create_response(
        message="Database is healthy" if db_healthy else "Database is unhealthy",
        data={"status": "healthy" if db_healthy else "unhealthy"},
        success=db_healthy
    )
