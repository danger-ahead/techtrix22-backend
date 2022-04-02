from pydantic import Field, BaseModel


class Sponsor(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    image: str = Field(...)
    links: list[str] = Field(...)
    id: int = Field(...)

    class Config:
        arbitrary_types_allowed = True
