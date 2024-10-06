from typing import Iterable

from lecture_2.hw.shop_api.store.models import Cart, Item
from lecture_2.hw.shop_api.item.contracts import ItemRequest

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

    return info


def get_one_cart(id: int) -> Cart | None:
    if id not in _data_cart:
        return None

    return _data_cart[id]


def get_many_carts(offset: int = 0, limit: int = 10, 
                   min_price: float = None, max_price: float = None,
                   min_quantity: int = None, max_quantity: int = None) -> Iterable[Cart]:
    for id in range(offset, offset + limit):
        if id in _data_cart:
            ret = 1
            if min_price:
                for item in _data_cart[id].items:
                    if item.price < min_price:
                        ret = 0
            if max_price:
                for item in _data_cart[id].items:
                    if item.price > max_price:
                        ret = 0
            quantity = sum(item.quantity for item in _data_cart[id].items)
            if min_quantity:
                if quantity < min_quantity:
                    ret = 0
            if max_quantity:
                if quantity > max_quantity:
                    ret = 0
            if ret == 1:
                yield _data_cart[id]


def get_one_item(id: int) -> Item | None:
    if id not in _data_item or _data_item[id].deleted:
        return None

    return _data_item[id]


def get_many_items(offset: int = 0, limit: int = 10,
                   min_price: float = None, max_price: float = None,
                   show_deleted: bool = False) -> Iterable[Item]:
    for id in range(offset, offset + limit):
        if id in _data_item:
            ret = 1
            if not show_deleted:
                if _data_item[id].deleted:
                    ret = 0
            if min_price:
                if _data_item[id].price > max_price:
                    ret = 0
            if max_price:
                if _data_item[id].price < min_price:
                    ret = 0
            if ret == 1:
                yield _data_item[id]


def put_item(id, info):
    if id not in _data_item:
        return None
    info = info.as_item_info(id)
    _data_item[id] = info
    return info


def delete_item(id):
    if id not in _data_item:
        return None
    _data_item[id].deleted = True
    return _data_item[id]

def patch_item(id, info):
    if id not in _data_item:
        return None
    if info.deleted != _data_item[id].deleted:
        return None
    info = info.as_item_info(id)
    _data_item[id] = info
    return info