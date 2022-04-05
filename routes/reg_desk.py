import datetime
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

import config
from models.reg_desk import RegDesk
from models.registration_pay import RegistrationPay
from oauth2 import create_access_token, verify_access_token

route = APIRouter(prefix="/reg_desk", tags=["Registration_Desk"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# sgnup api
@route.post("/signup", status_code=201)
async def signup(response: Response, reg_desk: RegDesk):
    try:
        reg_desk_db = config.techtrix_db["reg_desk"]
        if reg_desk.password.__contains__("/"):
            response.status_code = 200
            return {"success": False}

        reg_desk_db.insert_one(
            {
                "_id": reg_desk.id,
                "name": reg_desk.name,
                "password": reg_desk.password,
                "amt_collected_7": reg_desk.amt_collected_7,
                "amt_collected_8": reg_desk.amt_collected_8,
                "amt_collected_9": reg_desk.amt_collected_9,
            }
        )
        return {"success": True}

    except HTTPException as e:
        raise HTTPException(status_code=204, detail="error")


# login api
@route.post("/login/{email}/{password}", status_code=201)
def login(response: Response, email: str, password: str):
    reg_desks = config.techtrix_db["reg_desk"]
    reg_desk_obj = reg_desks.find_one({"_id": email})

    if reg_desk_obj is None:
        raise HTTPException(status_code=404, detail="user not found")

    else:
        if password == reg_desk_obj["password"]:
            return create_access_token(data={"email": email})
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")


# get the reg_desk obj
@route.get("/reg_desk_obj", status_code=200)
def get_reg_desk_obj(token: str = Depends(oauth2_scheme)):
    reg_desk = config.techtrix_db["reg_desk"]

    reg_desk_user_email = verify_access_token(token)
    reg_desk_user = reg_desk.find_one(
        {"_id": reg_desk_user_email},
        {"amt_collected_7": 1, "amt_collected_8": 1, "amt_collected_9": 1},
    )

    if reg_desk_user is None:
        raise HTTPException(status_code=404, detail="user not found")

    else:
        return reg_desk_user


# collect api
@route.put("/collect/{amount}", status_code=200)
def collect_fee(
    amount: str,
    registration_pay: RegistrationPay = Body(...),
    token: str = Depends(oauth2_scheme),
):
    registrations = config.techtrix_db["registrations"]
    participants = config.techtrix_db["participants"]
    reg_desk = config.techtrix_db["reg_desk"]

    for i in registration_pay.general_fees:
        participant = participants.find_one(
            {"email": i}, {"email": 1, "general_fees": 1}
        )
        if not participant["general_fees"]:
            participants.update_one({"email": i}, {"$set": {"general_fees": True}})

    for i in registration_pay.reg_id:
        registration = registrations.find_one({"_id": i}, {"_id": 1, "paid": 1})
        if registration["paid"] is False:
            registrations.update_one({"_id": i}, {"$set": {"paid": True}})

    # updating the collection amount
    reg_desk_user_email = verify_access_token(token)
    reg_desk_user = reg_desk.find_one({"_id": reg_desk_user_email})

    amt_collected_7 = reg_desk_user["amt_collected_7"]
    amt_collected_8 = reg_desk_user["amt_collected_8"]
    amt_collected_9 = reg_desk_user["amt_collected_9"]

    current_time = datetime.datetime.now()
    day = str(current_time.day)

    if day == "7":
        amt_collected_7 += int(amount)
        reg_desk.update_one(
            {"_id": reg_desk_user_email}, {"$set": {"amt_collected_7": amt_collected_7}}
        )
    elif day == "8":
        amt_collected_8 += int(amount)
        reg_desk.update_one(
            {"_id": reg_desk_user_email}, {"$set": {"amt_collected_8": amt_collected_8}}
        )
    elif day == "9":
        amt_collected_9 += int(amount)
        reg_desk.update_one(
            {"_id": reg_desk_user_email}, {"$set": {"amt_collected_9": amt_collected_9}}
        )

    return {"success": "true"}
