from .portfolio import Portfolio


class Account:
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def buying_power(self) -> float:
        pass

    @property
    def total_positions_value(self) -> float:
        pass

    @property
    def day_trades_remaining(self) -> float:
        pass

    @property
    def max_funds_usable(self) -> float:
        pass

    @property
    def portfolio(self) -> Portfolio:
        pass
