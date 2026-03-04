import uuid
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.member import MemberCreate
from app.repositories import member_repo


def _serialize_member(member):
    """Convert comma-separated DB strings back to lists for API responses."""
    member.roles = member.roles.split(",") if member.roles else []
    member.excite_reasons = member.excite_reasons.split(",") if member.excite_reasons else []
    return member


def create_member(db: Session, data: MemberCreate):
    # Duplicate check
    if member_repo.check_duplicate(db, data.site_id, data.whatsapp_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "error": {
                    "code": "DUPLICATE_MEMBER",
                    "message": "A member with this WhatsApp number already exists for this site.",
                },
            },
        )

    member_data = {
        "id": str(uuid.uuid4()),
        "site_id": data.site_id,
        "name": data.name,
        "roles": ",".join(data.roles),
        "other_role": data.other_role,
        "purpose": data.purpose,
        "media_links": data.media_links,
        "excite_reasons": ",".join(data.excite_reasons),
        "whatsapp_opt_in": data.whatsapp_opt_in,
        "whatsapp_number": data.whatsapp_number,
        "status": "pending",
    }

    member = member_repo.create_member(db, member_data)
    return member


def list_members(
    db: Session,
    site_id: Optional[str],
    status: Optional[str],
    search: Optional[str],
    page: int,
    page_size: int,
):
    if page_size > 100:
        page_size = 100

    items, total = member_repo.get_members(
        db,
        site_id=site_id,
        status=status,
        search=search,
        page=page,
        page_size=page_size,
    )
    return [_serialize_member(m) for m in items], total


def get_member_count(db: Session, site_id: Optional[str]):
    return member_repo.count_approved_members(db, site_id=site_id)
