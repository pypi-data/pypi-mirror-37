from enum import Enum
from typing import Generic, TypeVar

from .equity import Equity

E = TypeVar('E', bound=Equity)


class OrderType(Enum):
    MARKET = 0
    LIMIT = 1
    STOP = 2

    def __str__(self):
        return self.name


class OrderStatus(Enum):
    PENDING = 0
    FULFILLED = 1
    CANCELED = 2
    FAILED = 3

    def __str__(self):
        return self.name


# pylint: disable=E1136
class Order(Generic[E]):
    def __init__(self,
                 equity: E,
                 quantity,
                 price,
                 order_type: OrderType=OrderType.MARKET,
                 order_status: OrderStatus=OrderStatus.PENDING):
        self._equity = equity
        self._quantity = quantity
        self._price = price
        self._order_type = order_type
        self._order_status = order_status

    def to_dict(self):
        return {
            'equity': self.equity.to_dict(),
            'price': '%.2f' % self.price,
            'quantity': self.quantity,
            'type': str(self.order_type),
            'status': str(self.order_status)
        }

    def __repr__(self):
        return '[$%.2f %s %s x%d]' % (self.price, self.equity, self.order_type, self.quantity)

    @property
    def equity(self) -> E:
        return self._equity

    @property
    def quantity(self) -> int:
        return self._quantity

    @property
    def price(self) -> float:
        return self._price

    @property
    def order_type(self) -> OrderType:
        return self._order_type

    @property
    def order_status(self) -> OrderStatus:
        return self._order_status
