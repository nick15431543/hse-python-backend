from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt

from store.models import Cart
import store.queries

router_cart = APIRouter(prefix="/cart")

@router_cart.get(
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
async def get_cart_by_id(id: int) -> Cart:
    return store.queries.get_one_cart(id)

@router_cart.get("/")
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
) -> list[Cart]:
    return [cart for cart in store.queries.get_many_carts(offset, limit)]

@router_cart.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response):
    id = store.queries.add_cart()
    response.headers["location"] = f"/cart/{id}"
    return response

