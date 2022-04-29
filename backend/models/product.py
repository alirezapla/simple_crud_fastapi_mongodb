from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ProductSchema(BaseModel):
    name: Optional[str] = Field(...)
    price: Optional[float]
    description: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "foo",
                "price": 2000.5,
                "description": "product A",
            }
        }


class ProductId(ProductSchema):
    uid: int
    name: str = None

    class Config:
        orm_mode = True
