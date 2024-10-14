from typing import Iterable
from fastapi import HTTPException
from http import HTTPStatus
from .models import(
    ItemInfo,
    ItemEntity,
    ItemCartInfo,
    PatchItemInfo,
    CartInfo,
    CartEntity,
)

item_data = dict[int, ItemInfo]()
cart_data = dict[int, CartInfo]()

def item_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

def cart_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1
        
cart_id_gen = cart_id_generator()

item_id_gen = item_id_generator()

# CRUD операции
def add_item(info: ItemInfo) -> ItemEntity:
    id = next(item_id_gen)
    item_data[id] = info
    
    return ItemEntity(id, info)

def delete_item(id: int) -> ItemEntity:
    if id in item_data:
        item_data[id].deleted = True
        return ItemEntity(id=id,info=item_data[id])   
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
def get_one_item(id: int) -> ItemEntity | None:
    if id not in item_data or item_data[id].deleted == True:
        return None
    else:
        return ItemEntity(id=id,info=item_data[id])

def get_many_items(offset:  int = 0, limit: int = 10, min_price: float | None = None, max_price: float | None = None, show_deleted: bool = False) -> Iterable[ItemEntity]:
    
    filtered_data = {
        item_id: info for item_id, info in item_data.items() if
        (min_price is None or info.price >= min_price) and
        (max_price is None or info.price <= max_price) and
        (show_deleted is True or info.deleted == False)  
    }
    curr = 0
    for id, info in filtered_data.items():
        if offset <= curr < offset + limit:
            yield ItemEntity(id=id, info=info)
        curr += 1

def put_item(id: int, new_info: ItemInfo) -> ItemEntity | None:  
    if id in item_data:
        item_data[id] = new_info
        return ItemEntity(id=id,info=new_info)
    else:
        return None
    
def patch_item(id: int, patch_info: PatchItemInfo) -> ItemEntity | None:
    if id not in item_data or item_data[id].deleted == True:
        return None
    
    if patch_info.name is not None:
        item_data[id].name = patch_info.name
    
    if patch_info.price is not None:
        item_data[id].price = patch_info.price
    
    return ItemEntity(id=id,info=item_data[id])
    



def add_cart() -> id:
    id = next(cart_id_gen)
    cart_data[id] = CartInfo(items=[],price=0.00)
    
    return id

def add_item_to_cart(cart_id: int, item_id: int) -> CartEntity | None:
    if cart_id not in cart_data or item_id not in item_data:
        return None
    else:
        if item_id in cart_data[cart_id].items:
            cart_data[cart_id].items[item_id].quantity += 1
        else: 
            item_in_cart = ItemCartInfo(
                id=item_id,
                name=item_data[item_id].name,
                price=item_data[item_id].price,
                quantity=1,
                available=not item_data[item_id].deleted
            )
            cart_data[cart_id].items.append(item_in_cart)
        
        cart_data[cart_id].price = CartEntity(id=cart_id, info=cart_data[cart_id]).calculate_total_price()

        return CartEntity(id=cart_id, info=cart_data[cart_id])

def get_one_cart(id: int) -> CartEntity | None:
    if id not in cart_data:
        return None
    else:
        return CartEntity(id=id,info=cart_data[id])

def get_many_carts(offset:  int = 0, limit: int = 10, min_price: float | None = None, max_price: float | None = None, min_quantity: int | None = None, max_quantity: int | None = None) -> Iterable[CartEntity]:
    filtered_data = {
        cart_id: info for cart_id, info in cart_data.items() if
        (min_price is None or info.price >= min_price) and
        (max_price is None or info.price <= max_price) and
        (min_quantity is None or len(info.items) <= min_quantity) and
        (max_quantity is None or len(info.items) <= max_quantity)
    }
    curr = 0
    for id, info in filtered_data.items():
        if offset <= curr < offset + limit:
            yield CartEntity(id=id, info=info)
        curr += 1
