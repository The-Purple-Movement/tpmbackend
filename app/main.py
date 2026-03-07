from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tpm-web-kohl.vercel.app",
        "https://compassionai.netlify.app",
        "https://ai-compassion.netlify.app", # arjun-ms demo URL
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_origin_regex=r"https://deploy-preview-\d+--.*\.netlify\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/", include_in_schema=False)
def root():
    return {"status": "ok", "message": "TPM Backend is running"}

@app.on_event("startup")
def startup():
    init_db()