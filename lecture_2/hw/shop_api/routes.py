from http import HTTPStatus
from typing import Annotated
from lecture_2.hw.shop_api import queries

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat, PositiveFloat
from .contracts import(
    ItemResponse,
    ItemRequest,
    PatchItemRequest,
    CartResponse,
    CartRequest
)


router = APIRouter()

@router.get("/item")
async def get_item_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[PositiveFloat, Query()] = None,
        show_deleted: Annotated[bool, Query()] = False
    ) -> list[ItemResponse]:
        return[ItemResponse.from_item_entity(e) for e in queries.get_many_items(offset, limit, min_price, max_price, show_deleted)]
        
@router.get(
    "/item/{id}", 
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> ItemResponse:
    entity = queries.get_one_item(id)
    
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return ItemResponse.from_item_entity(entity)

@router.post("/item", status_code=HTTPStatus.CREATED)
async def post_item(info: ItemRequest, response: Response) -> ItemResponse:
    new_entity = queries.add_item(info)
    
    # as REST states one should provide uri to newly created resource in location header
    response.headers["location"] = f"/item/{new_entity.id}"
    
    return ItemResponse.from_item_entity(new_entity)

@router.patch(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully patched pokemon",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify pokemon as one was not found",
        },
    },
)
async def patch_item(id: int, info: PatchItemRequest) -> ItemResponse:
    patch_entity = queries.patch_item(id, info.as_patch_cart())

    if patch_entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    return ItemResponse.from_item_entity(patch_entity)

@router.put(
    "/item/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated or upserted item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    }
)
async def put_item(id: int, info: ItemRequest) -> ItemResponse:
    entity = queries.put_item(id,info)

    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )

    return ItemResponse.from_item_entity(entity)

@router.delete("/item/{id}")
async def delete_item(id: int) -> ItemResponse:
    deleted_item = queries.delete_item(id)
    
    return ItemResponse.from_item_entity(deleted_item)





@router.post("/cart", status_code=HTTPStatus.CREATED)
async def post_cart(response: Response) -> dict[str, int]:
    entity_id = queries.add_cart()

    # as REST states one should provide uri to newly created resource in location header
    response.headers["location"] = f"/cart/{entity_id}"

    return {"id": entity_id}

@router.get("/cart")
async def get_item_list(
        offset: Annotated[NonNegativeInt, Query()] = 0,
        limit: Annotated[PositiveInt, Query()] = 10,
        min_price: Annotated[NonNegativeFloat, Query()] = None,
        max_price: Annotated[PositiveFloat, Query()] = None,
        min_quantity: Annotated[NonNegativeInt, Query()] = None,
        max_quantity: Annotated[NonNegativeInt, Query()] = None
    ) -> list[CartResponse]:
        return(CartResponse.from_cart_entity(e) for e in queries.get_many_carts(offset, limit, min_price, max_price, min_quantity, max_quantity))
        
@router.get(
    "/cart/{id}", 
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> CartResponse:
    entity = queries.get_one_cart(id)
    
    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource /item/{id} was not found",
        )
    return CartResponse.from_cart_entity(entity)

@router.post("/cart/{cart_id}/add/{item_id}")
async def add_item_to_cart(cart_id: int, item_id: int) -> CartResponse:
    cart = queries.add_item_to_cart(cart_id, item_id)
    if not cart:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart or Item not found")
    return CartResponse.from_cart_entity(cart)