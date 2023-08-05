import logging
from .order_executor import OrderExecutor
from liveline.model import Stock, Options


class LiveLineOrder:
    def __init__(self, stock: OrderExecutor[Stock], options: OrderExecutor[Options]):
        self._stock = stock
        self._options = options

        if self._stock is not None and self._stock.logger is None:
            self._stock.logger = logging.getLogger('LL/StockOrderExec')
        if self._options is not None and self._options.logger is None:
            self._options.logger = logging.getLogger('LL/OptionsOrderExec')

    @property
    def stock(self) -> OrderExecutor[Stock]:
        return self._stock

    @property
    def options(self) -> OrderExecutor[Options]:
        return self._options
