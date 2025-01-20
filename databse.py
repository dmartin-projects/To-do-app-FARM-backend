from model import Todo
from bson import ObjectId
from datetime import datetime
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
DATABASE_URI = config.get("mongo_url")
if os.getenv("DATABASE_URI"): DATABASE_URI = os.getenv("DATABASE_URI") #ensures that if we have a system environment variable, it uses that instead

# mongodb driver
import motor.motor_asyncio




client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = client.TodoList
collection = database.todo

async def fetch_one_todo(id):
    document = await collection.find_one({"_id":ObjectId(id)})
    return document

async def fetch_all_between(start,end):
    todos = []
    cursor = collection.find({"created_at":{"$gte":start,"$lt":end}})
    async for document in cursor:
        todos.append(Todo(**document)) # i create a new Todo object using data from cursor 
    return todos


async def fetch_all_todos():
    todos = []
    cursor= collection.find({})
    async for document in cursor:
        todos.append(Todo(**document)) # i create a new Todo object using data from cursor 
    return todos


async def create_todo(todo):
    document = todo 
    result = await collection.insert_one(document)
    return document

async def update_todo(id, desc):
    await collection.update_one({"_id":ObjectId(id)}, {"$set": {"description": desc, "timestamp_updated_at": datetime.now()}})
    document = await collection.find_one({"_id":ObjectId(id)})
    return document

async def remove_todo(id):
    await collection.delete_one({"_id":ObjectId(id)})
    return True



# All methods used here are monogo methods 
# we have to be clear that mongo works with JSON so if we pass a todo object it must be a JSON