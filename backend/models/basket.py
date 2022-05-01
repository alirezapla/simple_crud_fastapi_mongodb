from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .product import ProductId


class ItemsQuantity(BaseModel):
    item_id: str
    quantity: int


class BasketSchema(BaseModel):
    items: dict = {}
    item_id_quantity: ItemsQuantity
    status: Optional[bool]
    created_at: Optional[datetime] = datetime.now()
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "item_id_quantity": {"item_id": " ", "quantity": 1},
                "status": False,
            }
        }


class AddToBasketSchema(BaseModel):
    items: dict = {}
    item_id_quantity: ItemsQuantity
    status: Optional[bool]
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "item_id_quantity": {"item_id": " ", "quantity": 1},
                "status": False,
            }
        }


class UpdateBasket(BaseModel):
    items: dict = {}
    item_id_quantity: ItemsQuantity
    status: Optional[bool]
    updated_at: Optional[datetime] = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "quantity": 1,
                "status": False,
            }
        }


class BasketReadWithProducts(BasketSchema):
    items: List[ProductId] = []
