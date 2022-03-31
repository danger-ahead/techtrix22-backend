from fastapi import APIRouter, Depends, HTTPException

# import models, utils
import mongo_loader

techtrix_db = mongo_loader.get_cluster0()

route = APIRouter(prefix="/home", tags=["Home"])


# @route.post("/", status_code=201)
