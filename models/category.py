from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str = Field(None)
    category_id: int = Field(None)

    class Config:
        arbitrary_types_allowed = True
        # json_encoders = {ObjectId: str}
        # schema_extra = {
        #     "example": {
        #         "name": "Jane Doe",
        #         "email": "jdoe@example.com",
        #         "course": "Experiments, Science, and Fashion in Nanophotonics",
        #         "gpa": "3.0",
        #     }
        # }
