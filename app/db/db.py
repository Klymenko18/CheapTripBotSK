from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.models import Subscription

DATABASE_URL = "postgresql://postgres:postgres@db:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def save_subscription(user_id: int, month: str, price: int):
    db = SessionLocal()
    try:
        subscription = Subscription(user_id=user_id, month=month, price=price)
        db.add(subscription)
        db.commit()
    finally:
        db.close()

def get_all_subscribers():
    db = SessionLocal()
    try:
        subs = db.query(Subscription).filter(Subscription.user_id != 0).all()
        return subs
    finally:
        db.close()
