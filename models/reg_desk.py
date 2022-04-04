from pydantic import BaseModel, Field


class RegDesk(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    password: str = Field(...)
    amt_collected_7: int = Field(...)
    amt_collected_8: int = Field(...)
    amt_collected_9: int = Field(...)

    class Config:
        arbitrary_types_allowed = True
