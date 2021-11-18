from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import Todo

import databse

#import all ddbb methods 

from databse import (
    fetch_one_todo,
    fetch_all_todos,
    create_todo,
    update_todo,
    remove_todo,
    fetch_all_between
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RETRIEVE ALL TODOs OBJECTS

@app.get('/api/todo', tags=['todo-app'])
async def get_todo():
    response = await fetch_all_todos()
    return response
#=========================================
#=========================================

# RETRIEVE A TODO OBJECT BY ID 

@app.get('/api/todo/{id}', tags=['todo-app'], response_model=Todo)
async def get_todo_by_id(id:str):
    document = await fetch_one_todo(id)
    if document:
        return document
    raise HTTPException(404, f'there is no TODO item with title - {id}') 
#=========================================
#=========================================

# RETRIEVE A TODO LIST BETWEEN RANGE OF DATES

@app.get('/api/todos_by_date/{start,end}', tags=['todo-app'])
async def get_todo_between_date(start,end):
   
    document = await fetch_all_between(datetime.strptime(start,'%Y-%m-%d'),datetime.strptime(end,'%Y-%m-%d'))
    if document:
        return document
    raise HTTPException(404, f'there is no TODO item with title - {id}') 

#=========================================
#=========================================

# ADDING A NEW TODO 

@app.post('/api/todo', tags=['todo-app'], response_model=Todo)
async def add_todo(todo:Todo):

    if hasattr(todo, 'id'):
        delattr(todo, 'id')

    response = await create_todo(todo.dict(by_alias=True)) # we must cast Todo obj to JSON coz is how mongodb works 
    if response:
        return response

    raise HTTPException(400, "something went wrong | but request")

#=========================================
#=========================================


# editing TODO 

@app.put('/api/todo/{id}/', tags=['todo-app'],response_model=Todo)
async def update_todo(id:str,desc:str):
    response = await databse.update_todo(id,desc) # we must pay attention how we named methodds coz i named function and method of ddbb  equeal so it fell into a recursion error 
    if response:
        return response
    raise HTTPException(404, f'there is no TODO item with title - {id}') 

#=========================================
#=========================================


# DELETE A TODO  BY ID

@app.delete("/api/todo/{id}", tags=['todo-app'])
async def delete_todo(id:str):
    response = await remove_todo(id)
    if response:
        return "Successfully deleted todo"
    raise HTTPException(404, f"There is no todo with the title {id}")
    


