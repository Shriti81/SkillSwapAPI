# schemas.py
from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime
import json

class UserCreate(BaseModel):
    name: str
    email: str
    skills_offered: List[str]
    skills_needed: List[str]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    skills_offered: List[str]
    skills_needed: List[str]

    @field_validator("skills_offered", "skills_needed", mode="before")
    def parse_json_list(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return []
        return v

    model_config = {
        "from_attributes": True
    }

class MatchRequest(BaseModel):
    user_id: int

class SkillExchangeRequest(BaseModel):
    sender_id: int
    receiver_id: int
    skill_offered: str
    skill_received: str

class SkillExchangeResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    skill_offered: str
    skill_received: str
    timestamp: datetime  # ✅ included timestamp field

    model_config = {
        "from_attributes": True
    }
