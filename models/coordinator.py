from pydantic import Field, BaseModel


class Coordinator(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    role: (str) = Field(...)
    password: (str) = Field(...)

    class Config:
        arbitrary_types_allowed = True
