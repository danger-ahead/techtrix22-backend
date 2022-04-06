from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from oauth2 import create_access_token
import config
from models.coordinator import Coordinator
route = APIRouter(prefix="/coordinators", tags=["Coordinators"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@route.post("/signup", status_code=201)
async def signup(response: Response, coordinator_obj :Coordinator):
    try:
        coordinator_db = config.techtrix_db["coordinators"]
        print(coordinator_obj)
        if coordinator_obj.password.__contains__("/"):
            response.status_code = 200
            return {"success": False}

        coordinator_db.insert_one(
            {
                "_id": coordinator_obj.id,
                "name": coordinator_obj.name,
                "password": coordinator_obj.password,
                "role":coordinator_obj.role
            }
        )
        return {"success": True}

    except HTTPException as e:
        raise HTTPException(status_code=204, detail="error")
@route.post("/login/{email}/{password}", status_code=201)
def login(response: Response, email: str, password: str):
    coordinator_db = config.techtrix_db["coordinators"]
    coordinator_obj = coordinator_db.find_one({"_id": email})

    if coordinator_obj is None:
        raise HTTPException(status_code=404, detail="user not found")
    

    else:
        if password == coordinator_obj["password"]:
            return create_access_token(data={"email": email})
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")