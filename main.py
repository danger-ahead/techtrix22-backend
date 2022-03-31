from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from database import engine
# from routes import home
import mongo_loader


# models.Base.metadata.create_all(bind=engine)

mongo_loader.get_database()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router(home.route)


@app.get("/")
def root():
    return {"message": "Welcome to TechTrix\'22"}