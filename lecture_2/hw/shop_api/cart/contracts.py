from pydantic import BaseModel, ConfigDict

from store.models import Cart

class CartResponse(BaseModel):
    id: int
    items: list[dict]
    price: float


    def from_entity(self, entity: Cart):
        return CartResponse(
            id=entity.id,
            items=entity.items,
            published=entity.price,
        )