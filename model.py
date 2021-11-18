
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from datetime import datetime


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Todo(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    title:str
    description:str
    created_at: datetime = datetime.now()
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }