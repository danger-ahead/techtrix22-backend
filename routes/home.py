from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

import config

route = APIRouter(prefix="/home", tags=["Home"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
async def home(token: str = Depends(oauth2_scheme)):
    if check_token(token):

        list_popular_events = []
        list_flagship_events = []
        list_category_events = []

        events = config.techtrix_db["events"]
        categories = config.techtrix_db["categories"]

        popular_events = list(events.find({"popular": True}))
        flagship_events = list(events.find({"flagship": True}))

        if popular_events.__len__() is not 0:
            for i in popular_events:
                list_popular_events.append(i)

        if flagship_events.__len__() is not 0:
            for i in flagship_events:
                list_flagship_events.append(i)

        category_events = list(categories.find())
        if category_events.__len__() is not 0:
            for i in category_events:
                list_category_events.append(i["_id"])

        return {
            "popular": list_popular_events,
            "flagship": list_flagship_events,
            "categories": list_category_events,
            "trending": config.trending_searches,
        }
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
