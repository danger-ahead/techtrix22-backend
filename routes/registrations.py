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


# @route.get("/team/{search_term}", status_code=200)
# async def get_total_fee(search_term: str, token: str = Depends(oauth2_scheme)):
#     if check_token(token):
#         teams = config.techtrix_db["teams"]
#         participants = config.techtrix_db["participants"]
#         events = config.techtrix_db["events"]

#         team = teams.find_one({"_id": search_term})
#         if team is None:
#             raise HTTPException(status_code=204, detail="team not found")

#         general_fee = {}
#         event_fee = {}

#         members_list = team["members"]
#         events_dict = team["events"]

#         for i in members_list:
#             participant = participants.find_one({"phone": i})
#             if participant["general_fees"] == False:
#                 general_fee[participant["name"]] = config.general_fees

#         for i in events_dict:
#             print(i)
#             event = events.find_one({"_id": int(i)})
#             if not events_dict[i]:
#                 event_fee[event["name"]] = event["fee"]

#         return {"general_fee": general_fee, "event_fee": event_fee}

#     else:
#         raise HTTPException(status_code=401, detail="Unauthorized")


# @route.get("/participant/{search_term}", status_code=200)
# async def get_general_fee(search_term: str, token: str = Depends(oauth2_scheme)):
#     if check_token(token):
#         participants = config.techtrix_db["participants"]

#         participant = participants.find_one({"phone": int(search_term)})

#         if participant is None:
#             raise HTTPException(status_code=204, detail="participant not found")

#         if participant["general_fees"] == False:
#             return {participant["name"]: config.general_fees}

#         else:
#             raise HTTPException(status_code=409, detail="already paid")

#     else:
#         raise HTTPException(status_code=401, detail="Unauthorized")
