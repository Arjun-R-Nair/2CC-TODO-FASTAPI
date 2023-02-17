from pydantic import BaseModel

class ToDoItem(BaseModel):
    description: str
    priority: int
    completed: bool = False
