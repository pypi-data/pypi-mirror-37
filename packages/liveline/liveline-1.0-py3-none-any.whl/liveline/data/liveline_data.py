import logging
from .data_provider import DataProvider
from liveline.model import Stock, Options, Account


class LiveLineData:
    def __init__(self, account: Account, stock: DataProvider[Stock], options: DataProvider[Options]):
        self._account = account
        self._stock = stock
        self._options = options

        if self._stock is not None and self._stock.logger is None:
            self._stock.logger = logging.getLogger('LL/StockDataProvider')
        if self._options is not None and self._options.logger is None:
            self._options.logger = logging.getLogger('LL/OptionsDataProvider')

    @property
    def account(self) -> Account:
        return self._account

    @property
    def stock(self) -> DataProvider[Stock]:
        return self._stock

    @property
    def options(self) -> DataProvider[Options]:
        return self._options
