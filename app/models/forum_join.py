from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from app.db.session import Base


class ForumJoin(Base):
    __tablename__ = "forum_join_requests"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    country = Column(String, nullable=False)
    city = Column(String, nullable=False)
    organization = Column(String, nullable=True)
    role = Column(String, nullable=True)
    interests = Column(JSON, nullable=False)
    other_interest = Column(JSON, nullable=True)
    newsletter = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
