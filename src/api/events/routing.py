import os
from fastapi import APIRouter, Depends, HTTPException
from api.db.session import get_session
from sqlmodel import Session, select
from .model import (
    EventModel,
    EventListSchema,
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

@router.get("/", response_model=EventListSchema)
def read_events(session:Session=Depends(get_session)):
    # a bunch of items in a table
    query = select(EventModel).order_by(EventModel.id.desc()).limit(7)
    results = session.exec(query).all()
    return {
        "results": results,
        "count": len(results)
    }


@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id:int, session:Session=Depends(get_session)):
    # a single row
    queue = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(queue).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.post("/", response_model=EventModel)
def create_event(payload:EventCreateSchema, session:Session=Depends(get_session)):
    data = payload.model_dump() # payload -> dict -> pydantic
    obj = EventModel.model_validate(data);
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put("/{event_id}", response_model=EventModel)
def update_event(
        event_id:int,
        payload:EventUpdateSchema,
        session:Session=Depends(get_session)):
    queue = select(EventModel).where(EventModel.id == event_id)
    obj = session.exec(queue).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Event not found")

    data = payload.model_dump() # payload -> dict -> pydantic
    for k, v in data.items():
        setattr(obj, k, v)

    session.add(obj)
    session.commit()
    session.refresh(obj)

    return obj


# @router.delete("/{event_id}")
# def delete_event(
#         event_id:int,
#         session:Session=Depends(get_session)):
#     query = select(EventModel).where(EventModel.id == event_id)
#     obj = session.exec(query).first()
#     if not obj:
#         raise HTTPException(status_code=404, detail="Event not found")
    
#     session.delete(obj)
#     session.commit()
#     session.refresh(obj)
