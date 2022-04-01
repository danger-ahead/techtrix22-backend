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
    events = config.techtrix_db["events"]
    categories = config.techtrix_db["categories"]

    event_results = []
    category_results = []

    result = events.find()
    for i in result:
        if (i["name"]).lower().__contains__(search_term.lower()):
            event_results.append(i)

    result = categories.find()
    for i in result:
        if (i["name"]).lower().__contains__(search_term.lower()):
            category_results.append(i)

    if event_results.__len__() == 0 and category_results.__len__() == 0:
        raise HTTPException(status_code=204, detail="nothing found")

    return {"events": event_results, "categories": category_results}
