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
        # team = teams.find_one({"id": {"$regex": search_term, "$options": "i"}})
        team = teams.find_one({"_id": search_term})
        if team is None:
            raise HTTPException(status_code=204, detail="no team found")
        return team
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.post("/", status_code=201)
def add_team(team: Team = Body(...), token: str = Depends(oauth2_scheme)):
    try:
        if check_token(token):
            teams = config.techtrix_db["teams"]
            teams.insert_one(
                {
                    "_id": team.id,
                    "members": team.members,
                    "contact": team.contact,
                    "image": team.image,
                    "event": team.event,
                }
            )
            return team
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))
