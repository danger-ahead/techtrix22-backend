from pydantic import BaseModel, Field


class Category(BaseModel):
    id: str = Field(None)

    class Config:
        arbitrary_types_allowed = True
