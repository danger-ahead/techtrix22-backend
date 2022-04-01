from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.participant import Participant

route = APIRouter(prefix="/participants", tags=["Participants"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def get_participants(token: str = Depends(oauth2_scheme)):
    if check_token(token):
        participants = config.techtrix_db["participants"]
        participants = list(participants.find())
        if participants.__len__() == 0:
            raise HTTPException(
                status_code=204, detail="Nothing yet added to the participants"
            )
        return participants
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.get("/{email}", status_code=200)
def get_participants(email: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        participants = config.techtrix_db["participants"]
        participants = participants.find_one({"email": email})
        if participants == None:
            raise HTTPException(
                status_code=204, detail="nothing yet added to the participants"
            )
        return participants
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.post("/", status_code=201)
def post_participant(
    participant: Participant = Body(...), token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        participants = config.techtrix_db["participants"]

        if (
            participants.find_one({"email": participant.email}) is not None
            or participants.find_one({"phone": participant.phone}) is not None
        ):
            raise HTTPException(status_code=409, detail="participant already exists")

        participants.insert_one(
            {
                "_id": participant.id,
                "name": participant.name,
                "email": participant.email,
                "phone": participant.phone,
                "institution": participant.institution,
                "general_fees": participant.general_fees,
                "gender": participant.gender,
            }
        )
        return {"success": "true"}

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.put("/general_fees/{id}/{general_fees}", status_code=204)
def update_participant(
    id: str, general_fees: bool, token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        participants = config.techtrix_db["participants"]

        if participants.find_one({"_id": id}):
            participants.update_one(
                {"_id": id}, {"$set": {"general_fees": general_fees}}
            )
            return {"success": "true"}
        else:
            raise HTTPException(status_code=404, detail="participant not found")

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
