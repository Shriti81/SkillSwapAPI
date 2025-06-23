import json
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import User,SkillExchange
from schemas import UserCreate,SkillExchangeRequest
from typing import List

def create_user(db: Session, user: UserCreate) -> User:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    db_user = User(
        name=user.name,
        email=user.email,
        skills_offered=json.dumps(user.skills_offered),
        skills_needed=json.dumps(user.skills_needed),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserCreate) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user.name
        db_user.email = user.email
        db_user.skills_offered = json.dumps(user.skills_offered)
        db_user.skills_needed = json.dumps(user.skills_needed)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> User | None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def find_matches(db: Session, user_id: int) -> List[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return []
    user_needed = set(json.loads(user.skills_needed))
    user_offered = set(json.loads(user.skills_offered))

    users = db.query(User).filter(User.id != user_id).all()
    matches = []
    for u in users:
        offered = set(json.loads(u.skills_offered))
        needed = set(json.loads(u.skills_needed))
        if user_needed & offered and user_offered & needed:
            matches.append(u)
    return matches
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def exchange_skills(db: Session, req: SkillExchangeRequest):
    exchange = SkillExchange(
        sender_id=req.sender_id,
        receiver_id=req.receiver_id,
        skill_offered=req.skill_offered,
        skill_received=req.skill_received,
    )
    db.add(exchange)
    db.commit()
    db.refresh(exchange)
    return exchange

def get_all_exchanges(db: Session):
    return db.query(SkillExchange).all()
