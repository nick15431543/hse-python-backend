from pydantic import BaseModel, ConfigDict

from lecture_2.hw.shop_api.store.models import Item

class ItemRequest(BaseModel):
    name: str = ''
    price: float = 0.0
    deleted: bool = False

    def as_item_info(self, id):
        return Item(id=id, name=self.name, price=self.price, deleted=self.deleted)