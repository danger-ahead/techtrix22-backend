from datetime import datetime
import random
from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.registration import Registration
from models.registration_pay import RegistrationPay

route = APIRouter(prefix="/registrations", tags=["Registrations"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# register for the event
@route.post("/", status_code=201)
async def register(
    registration: Registration = Body(...), token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        reg_id = str(datetime.now()) + " R " + str(random.randint(0, 99))

        registrations = config.techtrix_db["registrations"]
        participants = config.techtrix_db["participants"]
        events = config.techtrix_db["events"]
        reg_event_obj = events.find_one({"_id": int(registration.event)})

        for i in registration.participants:
            if participants.find_one({"email": i}) is None:
                # raise HTTPException(status_code=204, detail="participant doesn't exist")
                raise HTTPException(status_code=200, detail={"success": "false"})

        registrations.insert_one(
            {
                "_id": reg_id,
                "team_name": registration.team_name,
                "participants": registration.participants,
                "event": registration.event,
                "paid": registration.paid,
                "event_name": reg_event_obj["name"],
                "event_category": reg_event_obj["category"],
            }
        )
        return registration

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


# get all the events the participant has registered in
@route.get("/email/{search_term}", status_code=200)
async def check_events(search_term: str, token: str = Depends(oauth2_scheme)):
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


# get payment details from email
@route.get("/get_payment/email/{search_term}", status_code=200)
async def get_total_fee(search_term: str, token: str = Depends(oauth2_scheme)):
    if check_token(token):
        registrations = config.techtrix_db["registrations"]
        events = config.techtrix_db["events"]

        registration = registrations.find()

        # will be storing the email, no duplication
        participants_set = set()
        # will be storing the event list the participant has participated in
        events_list = []

        for reg in registration:
            if not reg["paid"]:
                participants = reg["participants"]
                for i in participants:
                    if search_term == i:
                        event = events.find_one({"_id": int(reg["event"])})
                        event_name = event["name"]
                        event_fee = event["fee"]

                        events_list.append({reg["_id"]: {event_name: event_fee}})
                        participants_set = participants_set.union(set(participants))

                        break

        general_fees = check_general_fees(participants_set)
        return {"general_fees": general_fees, "event_fees": events_list}

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@route.put("/pay", status_code=204)
async def get_total_fee(
    registration_pay: RegistrationPay = Body(...), token: str = Depends(oauth2_scheme)
):
    if check_token(token):
        registrations = config.techtrix_db["registrations"]
        participants = config.techtrix_db["participants"]

        for i in registration_pay.general_fees:
            participants.update_one({"email": i}, {"$set": {"general_fees": True}})

        for i in registration_pay.reg_id:
            registration = registrations.find_one({"_id": i})
            if registration is not None:
                registrations.update_one({"_id": i}, {"$set": {"paid": True}})

        return {"success": "true"}

    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
