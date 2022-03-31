from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import home, categories, events


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(home.route)
app.include_router(categories.route)
app.include_router(events.route)


@app.get("/")
def root():
    return {"message": "Welcome to TechTrix'22"}
