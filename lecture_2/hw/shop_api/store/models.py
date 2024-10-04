from dataclasses import dataclass, field

@dataclass
class Cart:
    id: int
    items: list[dict] = field(default_factory=list)
    price: float = 0

@dataclass
class Item:
    id: int
    name: str
    price: float
    deleted: bool = False
