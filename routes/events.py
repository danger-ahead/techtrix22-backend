from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.event import Event

route = APIRouter(prefix="/events", tags=["Events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This function fetches all events from db
@route.get("/", status_code=200)
def get_events():
    events = config.techtrix_db["events"]
    events = list(events.find())
    if events.__len__() == 0:
        raise HTTPException(status_code=204, detail="Nothing yet added to the events")
    return events


# This function fetches a particular event on the basis of event id
@route.get("/{id}", status_code=200)
def get_event_by_id(id: int):
    events = config.techtrix_db["events"]
    event = events.find_one({"_id": id})
    if event is None:
        raise HTTPException(status_code=204, detail="no event found")
    return event


# This function is used to create a new event
@route.post("/", status_code=201)
def post_event(event: Event = Body(...), token: str = Depends(oauth2_scheme)):
    if check_token(token):
        events = config.techtrix_db["events"]
        categories = config.techtrix_db["categories"]
        if categories.find_one({"_id": event.category}) is None:
            raise HTTPException(
                status_code=204,
                detail="category does not exist",
            )
        try:
            events.insert_one(
                {
                    "_id": event.id,
                    "name": event.name,
                    "category": event.category,
                    "desc": event.desc,
                    "rules": event.rules,
                    "contact": event.contact,
                    "fee": event.fee,
                    "tags": event.tags,
                    "regs_enabled": event.regs_enabled,
                    "popular": event.popular,
                    "flagship": event.flagship,
                    "min_participants": event.min_participants,
                    "max_participants": event.max_participants,
                    "info": event.info,
                    "poster": event.poster,
                }
            )
            return {"success": "true"}
        except Exception as e:
            raise HTTPException(status_code=409, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# This function lets you update details of a particular event params:event id
@route.put("/edit/{id}", status_code=204)
def update_event(id: int, event: dict, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        events = config.techtrix_db["events"]

        update_event = {}
        for key in event:
            if event[key] is not None:
                update_event[key] = event[key]

        if events.find_one({"_id": id}):
            events.update_one({"_id": id}, {"$set": update_event}, False)
            return {"success": "true"}
        else:
            raise HTTPException(status_code=404, detail="event not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
