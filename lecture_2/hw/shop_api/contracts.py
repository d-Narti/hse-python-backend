from __future__ import annotations
from pydantic import BaseModel, NonNegativeFloat, ConfigDict
from typing import List
from .models import(
    ItemEntity,
    ItemInfo,
    ItemCartInfo,
    PatchItemInfo,
    CartInfo,
    CartEntity,
)
class ItemResponse(BaseModel):
    id: int
    name: str
    price: NonNegativeFloat
    deleted: bool = False
    
    @staticmethod
    def from_item_entity(entity: ItemEntity) -> ItemResponse:
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
            deleted=entity.info.deleted
        )
    
class CartResponse(BaseModel):
    id: int
    items: List[ItemCartInfo]
    price: NonNegativeFloat
    
    @staticmethod
    def from_cart_entity(entity: CartEntity) -> CartResponse:
        return CartResponse(
            id=entity.id,
            items=entity.info.items,
            price=entity.info.price
        )
        
class ItemRequest(BaseModel):
    name: str
    price: NonNegativeFloat
    deleted: bool = False

    def as_item_info(self) -> ItemInfo:
        return ItemInfo(
            name=self.name, 
            price=self.price, 
            deleted=self.deleted
        )

class CartRequest(BaseModel):
    items: List[ItemCartInfo]
    price: NonNegativeFloat
    
    def as_cart_info(self) -> CartInfo:
        return CartInfo(
            items=self.items,
            price=self.price
        )
    
class PatchItemRequest(BaseModel):
    name: str | None = None
    price: NonNegativeFloat | None = None
    
    model_config = ConfigDict(extra="forbid")
    
    def as_patch_cart(self) -> PatchItemInfo:
        return PatchItemInfo(
            name=self.name,
            price=self.price
        )