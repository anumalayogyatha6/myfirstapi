from fastapi import FastAPI
from pydantic import BaseModel  # ← ADD THIS

app = FastAPI()

@app.get("/")
def home():
    return {"message": "My first API is working!"}

@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Hello {name}!"}

@app.get("/about")
def about():
    return {
        "name": "Yogyatha",
        "skills": ["Python", "FastAPI", "HTML", "CSS"],
        "goal": "Software Intern 2026",
        "college": "Siddhartha Academy of Higher Education"
    }

# ← ADD EVERYTHING BELOW

class Item(BaseModel):
    name: str
    description: str

@app.post("/items")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }