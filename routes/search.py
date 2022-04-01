from fastapi import APIRouter, Body, Depends, HTTPException

import config

route = APIRouter(prefix="/search", tags=["Search"])


@route.get("/search_category/{search_term}", status_code=200)
def get_events_under_category(search_term: str):
    events = config.techtrix_db["events"]

    results = []
    result = events.find({"category": search_term})
    for i in result:
        if (i["category"]).lower().find(search_term.lower()) is not -1:
            results.append(i)

    if results.__len__() == 0:
        raise HTTPException(status_code=204, detail="nothing found")

    return results


@route.get("/{search_term}", status_code=200)
def search(search_term: str):
    events_results = config.techtrix_db["events"]
    category_results = config.techtrix_db["categories"]

    results = []

    result = events_results.find()
    for i in result:
        if (i["name"]).lower().find(search_term.lower()) is not -1:
            results.append(i)

    if results.__len__() == 0:
        result = category_results.find()
        for i in result:
            if (i["name"]).lower().find(search_term.lower()) is not -1:
                results.append(i)

    if results.__len__() == 0:
        raise HTTPException(status_code=204, detail="nothing found")

    return results
