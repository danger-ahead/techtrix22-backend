from pydantic import BaseModel, Field


class Participant(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    email: str = Field(...)
    phone: int = Field(...)
    institution: str = Field(...)
    gender: str = Field(...)
    general_fees: bool = Field(...)

    class Config:
        arbitrary_types_allowed = True
