from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.event import Event

route = APIRouter(prefix="/events", tags=["Events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def get_events(token: str = Depends(oauth2_scheme)):
    if check_token(token):
        events = config.techtrix_db["events"]
        events = list(events.find())
        if events.__len__() == 0:
            raise HTTPException(
                status_code=204, detail="Nothing yet added to the events"
            )
        return events
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# TODO: add response model
@route.post("/", status_code=201)
def post_event(event: Event = Body(...), token: str = Depends(oauth2_scheme)):
    if check_token(token):
        events = config.techtrix_db["events"]
        categories = config.techtrix_db["categories"]
        if categories.find_one({"name": event.category}) is None:
            raise HTTPException(
                status_code=400,
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
                }
            )
            return {"success": "true"}
        except Exception as e:
            raise HTTPException(status_code=409, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
