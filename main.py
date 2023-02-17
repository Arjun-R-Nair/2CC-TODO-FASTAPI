from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
async def root():
    return "Hello World"

class Todo(BaseModel):
    title: str
    description: str
    completed: bool

todos = [
    {
        "id": 1,
        "title": "Todo 1",
        "description": "Todo 1 Description",
        "completed": False
    },
    {
        "id": 2,
        "title": "Todo 2",
        "description": "Todo 2 Description",
        "completed": True
    }
]

@app.get('/todos', status_code=status.HTTP_200_OK)
async def get_todos(title: str = ""):
    if title:
        results = [todo for todo in todos if title in todo['title']]
    else:
        results = todos
    return results

@app.get('/todos/{id}')
async def get_todo(id: int):
    todo = next((todo for todo in todos if todo['id'] == id), None)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo

@app.post('/todos', status_code=status.HTTP_201_CREATED)
async def create_todos(todo: Todo):
    id = max(todo['id'] for todo in todos) + 1
    todo_dict = todo.dict()
    todo_dict['id'] = id
    todos.append(todo_dict)
    return todo_dict

@app.put('/todos/{id}')
async def update_todo(id: int, todo: Todo):
    todo_index = next((index for index, todo in enumerate(todos) if todo['id'] == id), None)
    if todo_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todos[todo_index] = todo.dict()
    todos[todo_index]['id'] = id
    return todos[todo_index]

@app.delete('/todos/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int):
    todo_index = next((index for index, todo in enumerate(todos) if todo['id'] == id), None)
    if todo_index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    todos.pop(todo_index)
    return None
