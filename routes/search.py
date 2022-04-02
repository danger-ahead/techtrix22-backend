from fastapi import APIRouter, Body, Depends, HTTPException

import config

route = APIRouter(prefix="/search", tags=["Search"])


@route.get("/search_category/{search_term}", status_code=200)
def get_events_under_category(search_term: str):
    events = config.techtrix_db["events"]

    results = list(events.find({"category": {"$regex": search_term, "$options": "i"}}))

    if results.__len__() == 0:
        raise HTTPException(status_code=204, detail="nothing found")

    return results


@route.get("/{search_term}", status_code=200)
def search(search_term: str):
    events = config.techtrix_db["events"]
    categories = config.techtrix_db["categories"]

    event_results = list(
        events.find({"name": {"$regex": search_term, "$options": "i"}})
    )

    category_results = list(
        categories.find({"_id": {"$regex": search_term, "$options": "i"}})
    )

    if event_results.__len__() == 0 and category_results.__len__() == 0:
        raise HTTPException(status_code=204, detail="nothing found")

    return {"events": event_results, "categories": category_results}
