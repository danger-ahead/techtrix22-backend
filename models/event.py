from pickletools import int4
from pydantic import BaseModel, Field


class Event(BaseModel):
    name: str = Field(...)
    category: str = Field(...)
    desc: str = Field(...)
    rules: str = Field(...)
    contact: list[str] = Field(...)
    id: int = Field(...)
    fee: int = Field(...)
    tags: list[str] = Field(...)
    regs_enabled: bool = Field(...)
    popular: bool = Field(...)
    flagship: bool = Field(...)
    min_participants: int = Field(...)
    max_participants: int = Field(...)
    info: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
