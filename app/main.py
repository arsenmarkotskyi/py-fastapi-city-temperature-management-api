from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.routers import cities, temperatures
from app.database import engine, Base
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.services.weather_service import close_http_client

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing city data and their temperatures",
    version="1.0.0"
)

# Register routers
app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])


@app.get("/")
async def root():
    """
    Root endpoint for API health check.
    """
    return {
        "message": "City Temperature Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "cities": "/cities",
            "temperatures": "/temperatures"
        }
    }


@app.on_event("startup")
async def startup():
    """
    Creates database tables on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    """
    Closes database connections and HTTP client on application shutdown.
    
    Note: In SQLAlchemy 2.0+, AsyncEngine.dispose() is awaitable.
    For older versions, use engine.sync_engine.dispose() instead.
    """
    await engine.dispose()
    await close_http_client()


# Register error handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)  

