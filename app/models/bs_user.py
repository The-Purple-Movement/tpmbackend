import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func
from app.db.session import Base


def gen_uuid():
    return str(uuid.uuid4())


class BSUser(Base):
    __tablename__ = "bs_users"

    id = Column(String, primary_key=True, default=gen_uuid, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),
                        onupdate=func.now(), nullable=False)
