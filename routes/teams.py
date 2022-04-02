from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

import config
from models.team import Team

route = APIRouter(prefix="/teams", tags=["Teams"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def get_teams(token: str = Depends(oauth2_scheme)):
    if check_token(token):
        teams = config.techtrix_db["teams"]
        team = list(teams.find())
        if team.__len__() == 0:
            raise HTTPException(status_code=204, detail=[])
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
                    "name": team.name,
                    "contact_phone": team.contact_phone,
                    "image": team.image,
                    "role": team.role,
                }
            )
            return team
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))


@route.put("/edit/{id}", status_code=201)
def edit_teams(id: int, team: dict, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        teams = config.techtrix_db["teams"]
        updated_team = {}
        if teams.find_one({"_id": id}) is None:
            raise HTTPException(status_code=204, detail="team not found")
        else:
            for key in team:
                if team[key] is not None:
                    updated_team[key] = team[key]
            teams.update_one(
                {"_id": id},
                {
                    "$set": updated_team,
                },
            )
            return {"success": "true"}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
