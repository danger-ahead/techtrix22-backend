from pydantic import Field, BaseModel


class Registration(BaseModel):
    event: str = Field(...)
    participants: list[str] = Field(...)
    paid: bool = Field(...)
    team_name: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
