from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

import config
from models.participant import Participant

route = APIRouter(prefix="/participants", tags=["Participants"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# gets all the participants
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


# gets the particpant on the basis of the email
@route.get("/{email}", status_code=200)
def get_participants(email: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        participants = config.techtrix_db["participants"]
        participants = participants.find_one({"email": email})
        if participants == None:
            raise HTTPException(status_code=204, detail="no such participant found")
        return participants
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.post("/", status_code=201, response_model=Participant)
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
                "alt_phone": participant.alt_phone,
                "institution": participant.institution,
                "general_fees": participant.general_fees,
                "gender": participant.gender,
            }
        )
        return participant

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.put("/general_fees/{id}/{general_fees}", status_code=200)
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


@route.put("/{email}", status_code=200)
def update_participant(
    email: str, participant: dict, token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        participants = config.techtrix_db["participants"]

        update_items = {}
        for key in participant:
            if participant[key] is not None:
                update_items[key] = participant[key]

        if participants.find_one({"email": email}):
            participants.update_one({"email": email}, {"$set": update_items})
            return {"success": "true"}
        else:
            raise HTTPException(status_code=404, detail="participant not found")

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
