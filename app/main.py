from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.models.document import init_db
from app.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables and extensions are created on startup
    init_db()
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0"
    }


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API. Visit /docs for API documentation."
    }
