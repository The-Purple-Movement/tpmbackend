from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.schemas.member import (
    MemberCreate,
    MemberCreateEnvelope,
    MemberCreateResponse,
    MemberListResponse,
    MemberDetail,
    MemberCountResponse,
    PaginationMeta,
    VALID_STATUSES,
)
from app.services import member_service

router = APIRouter()


# ── DB dependency (same pattern as rest of codebase) ──────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── POST /members ─────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=MemberCreateEnvelope,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Join Form",
    description=(
        "Register a new member for a site. Replaces the Google Sheets webhook. "
        "Returns a pending member record. Duplicate WhatsApp numbers per site are rejected with 409."
    ),
)
def create_member(data: MemberCreate, db: Session = Depends(get_db)):
    member = member_service.create_member(db, data)
    return MemberCreateEnvelope(
        data=MemberCreateResponse.model_validate(member)
    )


# ── GET /members/count ────────────────────────────────────────────────────────
@router.get(
    "/count",
    response_model=MemberCountResponse,
    summary="Get Approved Member Count",
    description="Returns total approved member count, optionally filtered by site.",
)
def get_member_count(
    site_id: Optional[str] = Query(None, description="Filter by site ID, e.g. 'purple-movement'"),
    db: Session = Depends(get_db),
):
    count = member_service.get_member_count(db, site_id)
    return MemberCountResponse(data={"count": count, "site_id": site_id})


# ── GET /members ──────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=MemberListResponse,
    summary="List Members",
    description=(
        "Paginated, filterable list of all members. "
        "Supports filtering by site, status, and full-text name search."
    ),
)
def list_members(
    site_id: Optional[str] = Query(None, description="Filter by site, e.g. 'purple-movement'"),
    status: Optional[str] = Query(
        None,
        description="Filter by member status: pending | approved | rejected",
        pattern="^(pending|approved|rejected)$",
    ),
    search: Optional[str] = Query(None, description="Search by member name (case-insensitive)"),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page, max 100"),
    db: Session = Depends(get_db),
):
    members, total = member_service.list_members(
        db,
        site_id=site_id,
        status=status,
        search=search,
        page=page,
        page_size=page_size,
    )
    return MemberListResponse(
        data=[MemberDetail.model_validate(m) for m in members],
        meta=PaginationMeta(page=page, page_size=page_size, total=total),
    )
