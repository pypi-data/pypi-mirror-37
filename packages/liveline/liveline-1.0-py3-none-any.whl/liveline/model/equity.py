from enum import Enum
from datetime import datetime
from typing import TypeVar, Generic


class Equity:
    def __init__(self):
        pass

    def to_dict(self):
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def multipiler(self) -> float:
        pass


class Stock(Equity):
    def __init__(self, symbol):
        self._symbol = symbol

    def to_dict(self):
        return {'symbol': self.symbol}

    def __eq__(self, other):
        return isinstance(other, Stock) and self.symbol == other.symbol

    @property
    def name(self) -> str:
        return self.symbol

    def __repr__(self):
        return self.name

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def multipiler(self):
        return 1.0


class ETF(Equity):
    def __init__(self):
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def symbol(self) -> str:
        pass


OptionsUnderlyingEquity = TypeVar('OptionsUnderlyingEquity', Stock, ETF)


class OptionsType(Enum):
    CALL = 0
    PUT = 1

    def __str__(self):
        return self.name


# pylint: disable=E1136
class Options(Equity, Generic[OptionsUnderlyingEquity]):
    def __init__(self,
                 equity: OptionsUnderlyingEquity,
                 exp_date: datetime,
                 strike_price: float,
                 option_type: OptionsType):
        self._underlying_equity = equity
        self._exp_date = exp_date
        self._strike_price = strike_price
        self._option_type = option_type

    @property
    def name(self) -> str:
        return '%s %.2f %s %s' % (self.underlying_equity,
                                  self.strike_price,
                                  self.option_type,
                                  self.expiration_date.strftime('%Y-%m-%d'))

    def to_dict(self):
        return {
            'underlying_equity': self.underlying_equity.to_dict(),
            'strike_price': '%.2f' % self.strike_price,
            'expiration_date': self.expiration_date.strftime('%Y-%m-%d'),
            'type': str(self.option_type)
        }

    def __repr__(self):
        return '<%s>' % self.name

    def __eq__(self, other):
        return isinstance(other, Options) and \
            self.underlying_equity == other.underlying_equity and \
            self.strike_price == other.strike_price and \
            self.expiration_date == other.expiration_date and \
            self.option_type == other.option_type

    @property
    def multipiler(self):
        return 100.0

    @property
    def underlying_equity(self) -> OptionsUnderlyingEquity:
        return self._underlying_equity

    @property
    def expiration_date(self) -> datetime:
        return self._exp_date

    @property
    def strike_price(self) -> float:
        return self._strike_price

    @property
    def option_type(self) -> OptionsType:
        return self._option_type
