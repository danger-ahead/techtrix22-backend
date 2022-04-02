from pydantic import Field, BaseModel


class Team(BaseModel):
    id: int = Field(...)
    image: str = Field(...)
    name: str = Field(...)
    role: (str) = Field(...)
    contact_phone: int = Field(...)

    class Config:
        arbitrary_types_allowed = True
