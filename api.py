from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

# Create tables in database
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database connection helper
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request
class ItemCreate(BaseModel):
    name: str
    description: str

# GET all items from database
@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items

# POST - save item to database
@app.post("/items")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/")
def home():
    return {"message": "My first API is working!"}

@app.get("/about")
def about():
    return {
        "name": "Yogyatha",
        "skills": ["Python", "FastAPI", "HTML", "CSS"],
        "goal": "Software Intern 2026",
        "college": "Siddhartha Academy of Higher Education"
    }