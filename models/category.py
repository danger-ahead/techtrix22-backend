from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str = Field(None)
    id: int = Field(None)

    class Config:
        arbitrary_types_allowed = True
