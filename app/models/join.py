from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Join(Base):
    __tablename__ = "join_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    role = Column(String)