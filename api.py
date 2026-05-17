from fastapi import FastAPI

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
        "college" :  "siddhartha academy of higher education"
    }