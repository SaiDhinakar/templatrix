from fastapi import FastAPI
from contextlib import asynccontextmanager

from utils import settings, init_database
from routes import users_router, health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    init_database()
    yield
    # Shutdown (cleanup if needed)


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Include routers
app.include_router(users_router, prefix=settings.api_prefix)
app.include_router(health_router, prefix=settings.api_prefix)

@app.get('/')
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Templatrix FastAPI Template",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "docs_url": "/docs",
        "api_prefix": settings.api_prefix
    }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        'main:app',
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
    