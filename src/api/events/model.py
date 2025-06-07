from typing import List, Optional
import sqlmodel
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now


class EventModel(TimescaleModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    page: str = Field(index=True)
    description: Optional[str] = ""
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlmodel.DateTime(timezone=True),
        nullable=False
    )
    __chunk_time_interval__ = "INTERVAL 1 day"
    __drop_after__ = "INTERVAL 3 months"


class EventListSchema(SQLModel):
    results: List[EventModel]
    count: int


class EventCreateSchema(SQLModel):
    page: Optional[str] = Field(default=None) 
    description: Optional[str] = Field(default="my desc")


class EventUpdateSchema(SQLModel):
    description: str