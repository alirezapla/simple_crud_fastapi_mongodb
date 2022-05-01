from datetime import datetime
from typing import Optional

import bcrypt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DBModelMixin(BaseModel):
    created_at: Optional[datetime] = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(..., alias="updatedAt")
    id: Optional[int] = None


class UserSchema(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    national_id: str = Field(...)
    password: str = Field(...)

    @validator("national_id")
    def national_id_must_be_less_than_ten_digit(cls, v):
        if len(v) > 10:
            raise ValueError("must be less than ten digit")
        return v.title()

    @validator("national_id")
    def national_id_must_be_only_digit(cls, v):
        if not v.isdigit():
            raise ValueError("must be only digit")
        return v.title()

    @validator("password")
    def password_must_at_least_contain_one_special_character(cls, v):
        special_characters = '""!@#$%^&*()-+?_=,<>/""'
        if not any(c in special_characters for c in v):
            raise ValueError("must at least contain one special character")
        return v.title()

    @validator("password")
    def password_must_at_least_contain_one_upper_letter(cls, v):
        if v.islower() and v.find(" ") != -1:
            raise ValueError("must at least contain one upper letter")
        return v.title()

    @validator("password")
    def password_must_contain_alphabet_and_digit(cls, v):
        numeric_characters = "1234567890"
        if not any(c in numeric_characters for c in v):
            raise ValueError("must contain alphabet and digit")
        return v.title()

    @validator("password")
    def password_must_be_more_than_8_charechters(cls, v):
        if len(v) < 8:
            raise ValueError("must be more than 8 charechters")
        return v.title()

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "jdoe@x.edu.ng",
                "national_id": "0011223344",
                "password": "pass_word",
            }
        }


class UserOut(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    national_id: Optional[str]

    @validator("national_id")
    def national_id_must_be_less_than_ten_digit(cls, v):
        if len(v) > 10:
            raise ValueError("must be less than ten digit")
        return v.title()

    @validator("national_id")
    def national_id_must_be_only_digit(cls, v):
        if not v.isdigit():
            raise ValueError("must be only digit")
        return v.title()

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "jdoe@x.edu.ng",
                "national_id": "0011223344",
            }
        }


class UserInDB(DBModelMixin, UserSchema):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    salt: str = ""
    hashed_password: str = ""

    def check_password(self, password: str):
        return self._verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str):
        self.salt = self._generate_salt()
        self.hashed_password = self._get_password_hash(self.salt + password)

    @staticmethod
    def _generate_salt():
        return bcrypt.gensalt().decode()

    @staticmethod
    def _verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def _get_password_hash(password):
        return pwd_context.hash(password)
