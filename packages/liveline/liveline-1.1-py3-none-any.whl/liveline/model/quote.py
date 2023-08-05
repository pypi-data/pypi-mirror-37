from .equity import Equity


class Quote:
    def __init__(self, equity: Equity, ask_price, ask_size, bid_price, bid_size):
        self._equity = equity
        self._ask_price = ask_price
        self._ask_size = ask_size
        self._bid_price = bid_price
        self._bid_size = bid_size

    def __repr__(self):
        return '"%s @ $%.2f/$%.2f"' % (self.equity, self.ask_price, self.bid_price)

    @property
    def equity(self) -> Equity:
        return self._equity

    @property
    def ask_price(self) -> float:
        return self._ask_price

    @property
    def bid_price(self) -> float:
        return self._bid_price

    @property
    def ask_size(self) -> int:
        return self._ask_size

    @property
    def bid_size(self) -> int:
        return self._bid_size
