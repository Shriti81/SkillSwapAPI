from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    skills_offered = Column(String)
    skills_needed = Column(String)

    exchanges_sent = relationship("SkillExchange", back_populates="from_user", foreign_keys="[SkillExchange.from_user_id]")
    exchanges_received = relationship("SkillExchange", back_populates="to_user", foreign_keys="[SkillExchange.to_user_id]")

class SkillExchange(Base):
    __tablename__ = "skill_exchanges"

    id = Column(Integer, primary_key=True, index=True)
    from_user_id = Column(Integer, ForeignKey("users.id"))
    to_user_id = Column(Integer, ForeignKey("users.id"))
    skill_offered = Column(String)
    skill_requested = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    from_user = relationship("User", back_populates="exchanges_sent", foreign_keys=[from_user_id])
    to_user = relationship("User", back_populates="exchanges_received", foreign_keys=[to_user_id])
