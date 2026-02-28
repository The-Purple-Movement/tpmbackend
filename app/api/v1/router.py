from fastapi import APIRouter
from app.api.v1.endpoints import feedback, join

api_router = APIRouter()

api_router.include_router(
    feedback.router,
    prefix="/feedback",
    tags=["Website Feedback"]
)

api_router.include_router(
    join.router,
    prefix="/join",
    tags=["Community Join Requests"]
)