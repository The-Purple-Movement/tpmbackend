from sqlalchemy import Column, Integer, String, Boolean, Text
from app.db.session import Base


class Join(Base):
    __tablename__ = "join_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Site identifier — which website submitted this request
    site_id = Column(String, nullable=False)

    # Category: individual, organisation, government
    category = Column(String, nullable=False)

    # What defines you (dropdown value)
    what_defines_you = Column(String, nullable=False)

    # What do you want to share (paragraph text)
    what_to_share = Column(Text, nullable=False)

    # Optional link
    link = Column(String, nullable=True)

    # Anonymous toggle
    is_anonymous = Column(Boolean, default=False, nullable=False)

    # Personal details (optional — only filled when not anonymous)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)