import json


from typing import List
from .order import Order
from .position import Position

class Portfolio:
    def __init__(self):
        pass

    def to_dict(self):
        return {
            'orders': [o.to_dict() for o in self.orders],
            'positions': [p.to_dict() for p in self.positions]
        }


    @property
    def orders(self) -> List[Order]:
        pass


    @property
    def positions(self) -> List[Position]:
        pass
