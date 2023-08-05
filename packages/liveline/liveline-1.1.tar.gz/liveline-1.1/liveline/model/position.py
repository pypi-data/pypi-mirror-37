from .equity import Equity


class Position:
    def __init__(self):
        pass

    def to_dict(self):
        return {
            'equity': self.equity.to_dict(),
            'quantity': self.quantity,
            'average_cost': '%.2f' % self.average_cost
        }

    def __repr__(self):
        return "[%.0f x %s @ $%.2f]" % (self.quantity, self.equity, self.average_cost)

    @property
    def equity(self) -> Equity:
        pass

    @property
    def quantity(self) -> float:
        pass

    @property
    def average_cost(self) -> float:
        pass
