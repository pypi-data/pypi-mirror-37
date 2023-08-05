import logging
import pandas
from typing import Generic, TypeVar
from liveline.model import Equity, Quote


E = TypeVar('E', bound=Equity)


class DataProvider(Generic[E]):
    def __init__(self):
        self._logger = None

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    @logger.setter
    def logger(self, logger: logging.Logger):
        self._logger = logger

    def get_quote(self, equity: E) -> Quote:
        pass

    def get_historicals(self, equity: E) -> pandas.DataFrame:
        pass 
