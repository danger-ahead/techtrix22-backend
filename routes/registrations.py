from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.registration import Registration

route = APIRouter(prefix="/registrations", tags=["Registrations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def check_general_fees(email):
    participants = config.techtrix_db["participants"]
    participant = participants.find({"email": email})

    return participant["general_fees"]


@route.post("/", status_code=201)
async def register(
    registration: Registration = Body(...), token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        reg_id = registration.team_name.encode("ascii")
        registrations = config.techtrix_db["registrations"]
        if registrations.find_one({"team_name": reg_id}):
            raise HTTPException(status_code=409, detail="team name already exists")
        registrations.insert_one(
            {
                "_id": reg_id,
                "team_name": registration.team_name,
                "participants": registration.participants,
                "event": registration.event,
                "paid": registration.paid,
            }
        )
        return registration

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.get("/{search_term}", status_code=200)
async def get_total_fee(search_term: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        participants = config.techtrix_db["participants"]
        registrations = config.techtrix_db["registrations"]

        general_fees = []

        participant = participants.find({"email": search_term})
        general_fees.append(participant["general_fees"])

        participant_list = []

        registration = registrations.find()
        for reg in registration:
            participants = reg["participants"]
            for i in participants:
                if i.equals(search_term):
                    general_fees.append({})

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
