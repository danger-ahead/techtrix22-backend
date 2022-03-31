from fastapi import APIRouter, Depends, HTTPException
# import models, utils
# from database import get_db


route = APIRouter(
    prefix="/home",
    tags=['Home']
)


@route.post("/", status_code=201)
def add_user(user: User, db: Session = Depends(get_db)):
    user.password = utils.hash_password(user.password)
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise HTTPException(status_code=409, detail="User already exists")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"success": "true"}


@route.get("/{username}", response_model=UserOut)
def get_user_by_id(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    return user