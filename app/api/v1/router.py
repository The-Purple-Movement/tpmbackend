from fastapi import APIRouter
from app.api.v1.endpoints import feedback, join, members, forum_join

api_router = APIRouter()

api_router.include_router(
    feedback.router,
    prefix="/home/feedback",
    tags=["Website Feedback"]
)

api_router.include_router(
    join.router,
    prefix="/home/join",
    tags=["Community Join Requests"]
)

api_router.include_router(
    members.router,
    prefix="/members",
    tags=["Members"]
)

api_router.include_router(
    forum_join.router,
    prefix="/forum-join",
    tags=["Forum Join Requests"]
)