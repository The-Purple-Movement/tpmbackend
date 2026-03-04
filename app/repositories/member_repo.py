from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.member import Member


def create_member(db: Session, data: dict) -> Member:
    """Insert a new member row and return it."""
    obj = Member(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_member_by_id(db: Session, member_id: str) -> Optional[Member]:
    return db.query(Member).filter(Member.id == member_id).first()


def check_duplicate(db: Session, site_id: str, whatsapp_number: Optional[str]) -> bool:
    """Return True if a member with the same site_id + whatsapp_number already exists."""
    if not whatsapp_number:
        return False
    return (
        db.query(Member)
        .filter(
            Member.site_id == site_id,
            Member.whatsapp_number == whatsapp_number,
        )
        .first()
    ) is not None


def get_members(
    db: Session,
    site_id: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    page: int = 1,
    page_size: int = 20,
):
    """Paginated, filtered list of members."""
    query = db.query(Member)

    if site_id:
        query = query.filter(Member.site_id == site_id)
    if status:
        query = query.filter(Member.status == status)
    if search:
        query = query.filter(Member.name.ilike(f"%{search}%"))

    total = query.count()
    items = (
        query
        .order_by(Member.joined_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return items, total


def count_approved_members(db: Session, site_id: Optional[str] = None) -> int:
    query = db.query(func.count(Member.id)).filter(Member.status == "approved")
    if site_id:
        query = query.filter(Member.site_id == site_id)
    return query.scalar() or 0
