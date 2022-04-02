from pydantic import Field, BaseModel


class Sponsor(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    image: str = Field(...)
    links: list[str] = Field(...)
    id: int = Field(...)
