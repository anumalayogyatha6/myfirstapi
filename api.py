from fastapi import FastAPI, Depends, HTTPException 
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
# DELETE - remove item by id
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}
# UPDATE - modify existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item