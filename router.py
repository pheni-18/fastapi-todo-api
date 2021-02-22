from fastapi import APIRouter, Depends, HTTPException
from schemas import TodoCreate, TodoUpdate, Todo
from typing import List
from crud import TodoRepo
from sqlalchemy.orm import Session
from models import Base
from database import SessionLocal, engine
from constants import API_PREFIX


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix=API_PREFIX + "/todo",
)


@router.get("/", response_model=List[Todo])
async def get_todo_list(db: Session = Depends(get_db)):
    return TodoRepo.get_todo_list(db)


@router.post("/",  response_model=Todo)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return TodoRepo.create_todo(db, todo)


@router.get("/{id}", response_model=Todo)
async def get_todo(id_: int, db: Session = Depends(get_db)):
    db_todo = TodoRepo.get_todo(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.patch("/{id}",  response_model=Todo)
async def update_todo(id_: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = TodoRepo.get_todo(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo = TodoRepo.update_todo(db, id_, todo)
    return db_todo


@router.delete("/{id}")
async def delete_todo(id_: int, db: Session = Depends(get_db)):
    db_todo = TodoRepo.get_todo(db, id_)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    TodoRepo.delete_todo(db, id_)
