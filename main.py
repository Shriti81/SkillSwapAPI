# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine, Base
import json

app = FastAPI(title="SkillSwap API")

Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to SkillSwap API!"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.skills_offered = json.loads(user.skills_offered)
    user.skills_needed = json.loads(user.skills_needed)
    return user

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updated: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id, updated)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.skills_offered = json.loads(user.skills_offered)
    user.skills_needed = json.loads(user.skills_needed)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@app.post("/match/")
def match_users(request: schemas.MatchRequest, db: Session = Depends(get_db)):
    matches = crud.find_matches(db, request.user_id)
    result = []
    for user in matches:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "skills_offered": json.loads(user.skills_offered),
            "skills_needed": json.loads(user.skills_needed),
        })
    return result

@app.post("/exchange/", response_model=schemas.SkillExchangeResponse)
def exchange_skills(request: schemas.SkillExchangeRequest, db: Session = Depends(get_db)):
    return crud.exchange_skills(db, request)

@app.get("/exchanges/", response_model=list[schemas.SkillExchangeResponse])
def get_all_exchanges(db: Session = Depends(get_db)):
    return crud.get_all_exchanges(db)

@app.get("/match_ui", response_class=HTMLResponse)
def match_ui(request: Request):
    return templates.TemplateResponse("match.html", {"request": request})
