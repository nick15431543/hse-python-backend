from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from lecture_2.hw.shop_api.store.models import Item
import lecture_2.hw.shop_api.store.queries as queries
from lecture_2.hw.shop_api.item.contracts import ItemRequest

router_item = APIRouter(prefix="/item")

@router_item.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> Item:
    item = queries.get_one_item(id)
    if not item:
        raise HTTPException(
                    HTTPStatus.NOT_FOUND,
                    f"Request resource /item/{id} was not found",
                )
    return item

@router_item.get("/")
async def get_item_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeFloat, Query()] = None,
    max_price: Annotated[NonNegativeFloat, Query()] = None,
    show_deleted: Annotated[bool, Query()] = False,
) -> list[Item]:
    return [item for item in queries.get_many_items(offset, limit,
                                                    min_price, max_price,
                                                    show_deleted)]


@router_item.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_item(info: ItemRequest, response: Response):
    item = queries.add_item(info=info)
    response.headers["location"] = f"/item/{item.id}"
    return item


@router_item.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated or upserted item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    }
)
async def put_item(id: int, info: ItemRequest):
    item = queries.put_item(id, info)
    if item is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )
    return item


@router_item.delete(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully deleted item",
        },
    }
)
async def delete_item(id: int, response: Response):
    item = queries.delete_item(id)
    return item


@router_item.patch(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully patched item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    },
)
async def patch_item(id: int, info: ItemRequest):
    item = queries.patch_item(id, info)
    if item is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource /item/{id} was not found",
        )
    return item