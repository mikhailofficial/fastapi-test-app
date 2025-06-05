import os
from fastapi import APIRouter, Depends
from api.db.session import get_session
from sqlmodel import Session
from .model import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

@router.get("/")
def read_events() -> EventListSchema:
    # a bunch of items in a table
    return {
        "results": [
            {"id": 1},
            {"id": 54},
            {"id": 1488}
        ],
        "count": 3
    }


@router.get("/{event_id}")
def get_event(event_id:int) -> EventModel:
    # a single row
    return {
        "id": event_id
    }


@router.post("/", response_model=EventModel)
def create_event(payload:EventCreateSchema, session:Session=Depends(get_session)):
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data);
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema) -> EventModel:
    data = payload.model_dump() # payload -> dict -> pydantic
    return {
        "id": event_id,
        **data
    }