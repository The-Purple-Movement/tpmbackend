from sqlalchemy import Column, Integer, String, Text
from app.db.session import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    # Which site submitted this feedback
    site_id = Column(String, nullable=False)

    # Star rating (1–5)
    rating = Column(Integer, nullable=False)

    # Feedback paragraph
    message = Column(Text, nullable=False)