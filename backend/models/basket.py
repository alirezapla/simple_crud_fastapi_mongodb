from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from .product import ProductId


class BasketSchema(BaseModel):
    items: List[dict] = []
    items_uid_count: List[List[int]] = []
    status: Optional[bool]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "items_uid_count": "[['uid.0','count.0'],....,['uid.n','count.n']]",
                "status": False,
            }
        }


class UpdateBasket(BaseModel):
    items: List[dict] = []
    items_uid_count: List[List[int]]
    status: Optional[bool]
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "items_uid_count": "[['uid.0','count.0'],....,['uid.n','count.n']]",
                "status": False,
            }
        }


class BasketReadWithProducts(BasketSchema):
    items: List[ProductId] = []
