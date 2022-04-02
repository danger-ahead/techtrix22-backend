from pydantic import Field, BaseModel


class Team(BaseModel):
    members: list[int] = Field(...)
    id: str = Field(...)  # team name, team name has to be unique
    events: dict[str, bool] = Field(...)
    contact: int = Field(...)
    image: str = Field(...)
