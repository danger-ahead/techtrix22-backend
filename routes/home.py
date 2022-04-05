from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

import config

route = APIRouter(prefix="/home", tags=["Home"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def home(version_code: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        list_popular_events = []
        list_flagship_events = []
        list_category_events = []

        events = config.techtrix_db["events"]
        categories = config.techtrix_db["categories"]

        events_obj = list(events.find())
        for event in events_obj:
            if event["popular"]:
                list_popular_events.append(event)
            if event["flagship"]:
                list_flagship_events.append(event)

        category_events = list(categories.find())
        if category_events.__len__() != 0:
            for i in category_events:
                list_category_events.append(i["_id"])

        update_required = True if int(version_code) < 4 else False

        return {
            "popular": list_popular_events,
            "flagship": list_flagship_events,
            "categories": list_category_events,
            "trending": config.trending_searches,
            "update_required": update_required,
        }

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
