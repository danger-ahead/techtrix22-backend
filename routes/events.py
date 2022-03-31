from fastapi import APIRouter, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer

# import models, utils
import config
from models.event import Event

route = APIRouter(prefix="/events", tags=["Events"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@route.get("/", status_code=200)
def get_categories(token: str = Depends(oauth2_scheme)):
    if check_token(token):
        categories = config.techtrix_db["events"]
        categories = list(categories.find())
        if categories.__len__() == 0:
            raise HTTPException(
                status_code=204, detail="Nothing yet added to the events"
            )
        return categories
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
