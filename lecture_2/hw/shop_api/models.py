from dataclasses import dataclass
from pydantic import NonNegativeFloat, PositiveInt
from typing import List

@dataclass(slots=True)
class ItemInfo:
    name: str
    price: NonNegativeFloat
    deleted: bool = False

@dataclass(slots=True)
class ItemCartInfo:
    id: int
    name: str
    price: NonNegativeFloat
    quantity: PositiveInt 
    available: bool = True
    
@dataclass(slots=True)
class ItemEntity:
    id: int
    info: ItemInfo 

@dataclass(slots=True)
class PatchItemInfo:
    name: str | None = None
    price: NonNegativeFloat | None = None
    deleted: bool = False #?




@dataclass(slots=True)
class CartInfo:
    items: List[ItemCartInfo]
    price: NonNegativeFloat 
    
@dataclass(slots=True)
class CartEntity:
    id: int
    info: CartInfo
    
    def calculate_total_price(self) -> NonNegativeFloat:
        return sum(item.price * item.quantity for item in self.info.items if item.available)