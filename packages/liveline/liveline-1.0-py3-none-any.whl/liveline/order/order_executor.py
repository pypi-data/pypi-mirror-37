import logging
from typing import Generic, TypeVar, List
from liveline.model import Order, Equity, OrderType, OrderStatus


E = TypeVar('E', bound=Equity)


# pylint: disable=E1136
class OrderExecutor(Generic[E]):
    def __init__(self): 
        self._logger = None

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        self._logger = logger

    def place_order(self, equity: E, quantity: int, price: float, order_type=OrderType.MARKET) -> Order[E]:
        pass

    def cancel_order(self, order: Order[E]) -> Order[E]:
        pass


# pylint: disable=E1136
class PoolExecutor(OrderExecutor, Generic[E]):
    """
    This will not actually execut the orders, it will only store all orders
    in a order pool, which can be used to validate all orders.
    """

    def __init__(self):
        OrderExecutor.__init__(self)
        self._pool: List[Order] = list()

    @property
    def pool(self) -> List[Order]:
        return self._pool

    def place_order(self, equity: E, quantity: int, price: float, order_type=OrderType.MARKET) -> Order[E]:
        order = Order(equity, quantity, price, order_type=order_type)
        self._pool.append(order)
        return order

    def cancel_order(self, order: Order[E]) -> Order[E]:
        order.order_status = OrderStatus.CANCELED
        return order
