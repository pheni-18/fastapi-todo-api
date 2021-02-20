from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from crud import (
    get_todo_list as get_todo_list_, create_todo as create_todo_,
    get_todo as get_todo_, update_todo as update_todo_, delete_todo as delete_todo_
)
from models import Base
from schemas import TodoCreate, TodoUpdate, Todo
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/todo", response_model=List[Todo])
async def get_todo_list(db: Session = Depends(get_db)):
    return get_todo_list_(db)


@app.post("/api/todo",  response_model=Todo)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return create_todo_(db, todo)


@app.get("/api/todo/{id}", response_model=Todo)
async def get_todo(id_: int, db: Session = Depends(get_db)):
    db_todo = get_todo_(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@app.patch("/api/todo/{id}",  response_model=Todo)
async def update_todo(id_: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = get_todo_(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo = update_todo_(db, id_, todo)
    return db_todo


@app.delete("/api/todo/{id}")
async def delete_todo(id_: int, db: Session = Depends(get_db)):
    db_todo = get_todo_(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    delete_todo_(db, id_)
