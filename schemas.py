from pydantic import BaseModel


class TodoBase(BaseModel):
    title: str
    description: str
    done: bool


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        orm_mode = True
