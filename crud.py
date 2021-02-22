from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate


class TodoRepo:
    @staticmethod
    def get_todo(db: Session, id_: int):
        return db.query(Todo).filter(Todo.id == id_).first()

    @staticmethod
    def get_todo_list(db: Session):
        return db.query(Todo).all()

    @staticmethod
    def create_todo(db: Session, todo: TodoCreate):
        db_todo = Todo(title=todo.title, description=todo.description, done=todo.done)
        db.add(db_todo)
        db.commit()
        return db_todo

    @staticmethod
    def update_todo(db: Session, id_: int, todo: TodoUpdate):
        db_todo = db.query(Todo).filter(Todo.id == id_).first()
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.done = todo.done
        db.commit()
        return db_todo

    @staticmethod
    def delete_todo(db: Session, id_: int):
        db_todo = db.query(Todo).filter(Todo.id == id_)
        db_todo.delete()
        db.commit()
