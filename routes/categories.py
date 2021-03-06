from fastapi import APIRouter, Body, Depends, HTTPException
from auth import check_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

import config
from models.category import Category

route = APIRouter(prefix="/categories", tags=["Categories"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This function fetches all categories from db
@route.get("/", status_code=200)
def get_categories():
    categories = config.techtrix_db["categories"]
    categories = list(categories.find())
    if categories.__len__() == 0:
        raise HTTPException(
            status_code=204, detail="Nothing yet added to the categories"
        )
    return categories


# TODO: add response model
# This function is used create a new category in d
@route.post("/", status_code=201)
def post_category(category: Category = Body(...), token: str = Depends(oauth2_scheme)):
    if check_token(token):
        categories = config.techtrix_db["categories"]
        try:
            categories.insert_one({"_id": category.id})
            return category
        except Exception as e:
            raise HTTPException(status_code=409, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
