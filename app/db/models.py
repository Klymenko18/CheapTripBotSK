from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    month = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
