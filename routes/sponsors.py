from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from models.sponsor import Sponsor


import config


route = APIRouter(prefix="/sponsors", tags=["Sponsors"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def get_Sponsors():
    sponsors = config.techtrix_db["sponsors"]
    sponsor = list(sponsors.find())
    if sponsor.__len__() == 0:
        raise HTTPException(status_code=204, detail=[])
    return sponsor


@route.post("/", status_code=201)
def add_Sponsors(sponsor: Sponsor = Body(...), token: str = Depends(oauth2_scheme)):
    if check_token(token):
        try:
            sponsors = config.techtrix_db["sponsors"]
            sponsors.insert_one(
                {
                    "_id": sponsor.id,
                    "name": sponsor.name,
                    "description": sponsor.description,
                    "image": sponsor.image,
                    "links": sponsor.links,
                }
            )
            return {"success": "true"}
        except Exception as e:
            raise HTTPException(status_code=409, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
