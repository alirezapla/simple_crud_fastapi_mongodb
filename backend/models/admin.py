from pydantic import BaseModel, Field, EmailStr


class AdminModel(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "abbas boazar",
                "email": "abbas@boazar.com",
                "password": "pass_word"
            }
        }