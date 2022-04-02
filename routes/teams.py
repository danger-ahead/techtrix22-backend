from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

import config
from models.participant import Participant
from models.team import Team

route = APIRouter(prefix="/teams", tags=["Teams"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/search/{search_term}", status_code=200)
def get_teams(search_term: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        teams = config.techtrix_db["teams"]
        team = teams.find_one({"_id": {"$regex": search_term, "$options": "i"}})
        if team is None:
            raise HTTPException(status_code=204, detail="no team found")
        return team
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.post("/", status_code=201)
def add_team(team: Team = Body(...), token: str = Depends(oauth2_scheme)):
    if check_token(token):
        teams = config.techtrix_db["teams"]

        for i in team.members:
            participant = config.techtrix_db["participants"].find_one({"phone": i})
            if participant is None:
                raise HTTPException(
                    status_code=204, detail="participant not found: " + str(i)
                )

        teams.insert_one(
            {
                "_id": team.id,
                "members": team.members,
                "contact": team.contact,
                "image": team.image,
                "events": team.events,
            }
        )
        return team
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.put("/edit/{id}", status_code=201)
def edit_participated_events(
    id: str, updates: dict, token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        teams = config.techtrix_db["teams"]
        if teams.find_one({"_id": id}) is None:
            raise HTTPException(status_code=204, detail="team not found")
        else:
            teams.update_one(
                {"_id": id},
                {
                    "$set": updates,
                },
            )
            return {"success": "true"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.put("/edit/{id}", status_code=201)
def edit_participated_events(
    id: str, updates: dict, token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        teams = config.techtrix_db["teams"]
        if teams.find_one({"_id": id}) is None:
            raise HTTPException(status_code=204, detail="team not found")
        else:
            teams.update_one(
                {"_id": id},
                {
                    "$set": updates,
                },
            )
            return {"success": "true"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
