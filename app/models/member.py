import uuid
from sqlalchemy import (
    Column, String, Boolean, Text, ARRAY, DateTime, func
)
from app.db.session import Base


def gen_uuid():
    return str(uuid.uuid4())


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, default=gen_uuid, index=True)
    site_id = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)

    # roles is stored as a comma-separated string for broad DB compatibility;
    # the service layer converts to/from List[str]
    roles = Column(Text, nullable=False)          # e.g. "Student,Creator/Builder"
    other_role = Column(String, nullable=True)

    purpose = Column(Text, nullable=False)
    media_links = Column(Text, nullable=True)

    excite_reasons = Column(Text, nullable=False)  # comma-separated

    whatsapp_opt_in = Column(Boolean, default=False, nullable=False)
    whatsapp_number = Column(String, nullable=True)

    status = Column(String, default="pending", nullable=False)  # pending | approved | rejected

    certificate_id = Column(String, nullable=True)

    joined_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
