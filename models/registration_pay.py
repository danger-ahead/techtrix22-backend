from pydantic import Field, BaseModel


class RegistrationPay(BaseModel):
    general_fees: list[str] = Field(...)
    reg_id: list[str] = Field(...)

    class Config:
        arbitrary_types_allowed = True
