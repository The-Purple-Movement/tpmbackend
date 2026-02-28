from fastapi import FastAPI
from app.api.v1.router import api_router
from app.events.startup import init_db

app = FastAPI(
    title="TPM Backend",
    description="Central backend for TPM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)
app.include_router(api_router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "message": "TPM Backend is running"}

@app.on_event("startup")
def startup():
    init_db()