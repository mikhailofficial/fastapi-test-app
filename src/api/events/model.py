from typing import List, Optional
#from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field


class EventModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: Optional[str] = ""
    description: Optional[str] = ""


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: Optional[str] = Field(default=None) 
    description: Optional[str] = Field(default="my desc")


class EventUpdateSchema(SQLModel):
    description: str