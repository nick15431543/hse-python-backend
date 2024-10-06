from fastapi import FastAPI
import uvicorn
import sys
sys.path.append('../../../')


from lecture_2.hw.shop_api.cart import router_cart
from lecture_2.hw.shop_api.item import router_item

app = FastAPI(
    docs_url='/docs',
    openapi_url='/docs.json',
    title="Shop API",
)

app.include_router(router_cart)
app.include_router(router_item)
