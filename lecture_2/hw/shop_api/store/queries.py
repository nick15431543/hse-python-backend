from typing import Iterable

from .models import Cart, Item
from item.contracts import ItemRequest

_data_cart = dict[int, Cart]()
_data_item = dict[int, Item]()


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_id_cart_generator = int_id_generator()
_id_item_generator = int_id_generator()

def add_cart():
    _id = next(_id_cart_generator)
    _data_cart[_id] = Cart(id=_id)

    return _id

def add_item(info: ItemRequest):
    _id = next(_id_item_generator)
    info = info.as_item_info(_id)
    _data_item[_id] = info

    return _id

def get_one_cart(id: int) -> Cart | None:
    if id not in _data_cart:
        return None

    return _data_cart[id]


def get_many_carts(offset: int = 0, limit: int = 10) -> Iterable[Cart]:
    for id in range(offset, offset + limit):
        if id in _data_cart:
            yield _data_cart[id]

def get_one_item(id: int) -> Item | None:
    if id not in _data_item:
        return None

    return _data_item[id]


def get_many_items(offset: int = 0, limit: int = 10) -> Iterable[Item]:
    for id in range(offset, offset + limit):
        if id in _data_item:
            yield _data_item[id]