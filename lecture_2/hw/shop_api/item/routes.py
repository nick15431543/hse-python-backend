from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt

from store.models import Item
import store.queries
from .contracts import ItemRequest

router_item = APIRouter(prefix="/item")

@router_item.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested otem",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> Item:
    return store.queries.get_one_item(id)

@router_item.get("/")
async def get_item_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
) -> list[Item]:
    return [item for item in store.queries.get_many_items(offset, limit)]

@router_item.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_item(info: ItemRequest, response: Response):
    id = store.queries.add_item(info=info)
    response.headers["location"] = f"/item/{id}"
    return response

