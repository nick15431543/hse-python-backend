from fastapi import FastAPI
import uvicorn

from cart import router_cart
from item import router_item

app = FastAPI(title="Shop API")

app.include_router(router_cart)
app.include_router(router_item)
