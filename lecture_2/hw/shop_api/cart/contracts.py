from pydantic import BaseModel, ConfigDict

from lecture_2.hw.shop_api.store.models import Cart

class CartResponse(BaseModel):
    id: int
    items: list[dict] = []
    price: float = 0.0


    def from_entity(self, entity: Cart):
        return CartResponse(
            id=entity.id,
            items=entity.items,
            published=entity.price,
        )