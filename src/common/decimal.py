from decimal import Decimal as _Decimal
from typing import Union


class Decimal(_Decimal):
    pass


def to_string(value: Union[Decimal, int, str, float]): return format(round(Decimal(value), 4), '.4f')
