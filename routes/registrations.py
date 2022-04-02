from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.registration import Registration

route = APIRouter(prefix="/registrations", tags=["Registrations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.post("/", status_code=201)
async def register(
    registration: Registration = Body(...), token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        reg_id = registration.team_name.encode("ascii")
        registrations = config.techtrix_db["registrations"]
        participants = config.techtrix_db["participants"]

        if registrations.find_one({"team_name": reg_id}):
            raise HTTPException(status_code=409, detail="team name already exists")

        for i in registration.participants:
            if participants.find_one({"email": i}) is None:
                raise HTTPException(status_code=204, detail="participant doesn't exist")

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


@route.get("/email/{search_term}", status_code=200)
async def get_total_fee(search_term: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        registrations = config.techtrix_db["registrations"]
        registration = registrations.find()

        registration_list = []

        for reg in registration:
            participants = list(reg["participants"])
            for i in participants:
                if search_term == i:
                    registration_list.append(reg)
        return registration_list

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# function to check the general fees paid status
def check_general_fees(participant_set):
    participants_collection = config.techtrix_db["participants"]
    participants_dict = {}

    for participants in participant_set:
        individual_participant = participants_collection.find_one(
            {"email": participants}
        )
        if individual_participant["general_fees"] is False:
            participants_dict[participants] = config.general_fees

    return participants_dict


@route.get("/get_payment/email/{search_term}", status_code=200)
async def get_total_fee(search_term: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        participants = config.techtrix_db["participants"]
        registrations = config.techtrix_db["registrations"]

        registration = registrations.find()

        participants_set = set()

        for reg in registration:
            participants = reg["participants"]
            for i in participants:
                if search_term == i:
                    participants_set = participants_set.union(set(participants))
                    break

        general_fees = check_general_fees(participants_set)
        return {"general_fees": general_fees}

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
