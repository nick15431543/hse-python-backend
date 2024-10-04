from pydantic import BaseModel, ConfigDict

from store.models import Item

class ItemRequest(BaseModel):
    name: str
    price: float
    deleted: bool = False

    def as_item_info(self, id):
        return Item(id=id, name=self.id, price=self.price, deleted=self.deleted)