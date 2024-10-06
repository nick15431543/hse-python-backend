from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt, NonNegativeFloat

from lecture_2.hw.shop_api.store.models import Cart
import lecture_2.hw.shop_api.store.queries as queries

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
    cart = queries.get_one_cart(id)
    if not cart:
        raise HTTPException(
                HTTPStatus.NOT_FOUND,
                f"Request resource /cart/{id} was not found",
            )
    return cart

@router_cart.get("/")
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeFloat, Query()] = None,
    max_price: Annotated[NonNegativeFloat, Query()] = None,
    min_quantity: Annotated[NonNegativeInt, Query()] = None,
    max_quantity: Annotated[NonNegativeInt, Query()] = None,
) -> list[Cart]:
    return [cart for cart in queries.get_many_carts(offset, limit, 
                                                    min_price, max_price,
                                                    min_quantity, max_quantity)]

@router_cart.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def post_cart(response: Response):
    id = queries.add_cart()
    response.headers["location"] = f"/cart/{id}"
    return {"id": id}

