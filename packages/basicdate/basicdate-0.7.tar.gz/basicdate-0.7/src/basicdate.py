import datetime
import numbers
from json import JSONDecoder, JSONEncoder

import dateparser

VERSION = "0.7"
NAME = "basicdate"
AUTHOR = "Giovanni Bronzini"
AUTHOR_EMAIL = "g.bronzini@gmail.com"
DESCRIPTION = "A very basic set of Python classes for simple date manipulation"
LICENSE = "BSD 3-Clause"
URL = "https://github.com/GigiusB/basicdate"

class BasicDate:
    """
    >>> str(BasicDate('15/01/2018'))
    '15/01/2018'
    >>> repr(BasicDate('15/01/2018'))
    "BasicDate('15/01/2018')"
    >>> BasicDate().isocalendar() == datetime.date.today().isocalendar()
    True
    """
    __cache = {}
    def __new__(cls, day=None, date_formats=('%d/%m/%Y', '%Y-%m-%d', '%Y%m%d'), fail=True):
        _date = None
        if day is None:
            _date = datetime.date.today()
        try:
            if isinstance(day, BasicDate):
                _date = day._date
            elif isinstance(day, datetime.datetime):
                _date = day.date()
            elif isinstance(day, datetime.date):
                _date = day
            elif day:
                _date = dateparser.parse(day, date_formats=date_formats,
                                              settings={'DATE_ORDER': 'DMY'}).date()
        except:
            if fail:
                raise
            _date = datetime.date.today()

        if _date in BasicDate.__cache:
            return BasicDate.__cache[_date]
        else:
            o = object.__new__(cls)
            o._date = _date
            BasicDate.__cache[_date] = o
            return o

    def __str__(self, format='%d/%m/%Y'):
        return self._date.strftime(format)

    def __format__(self, format_spec: str) -> str:
        return self.__str__(format_spec)

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            return BasicDate(self._date + datetime.timedelta(days=float(other)))
        return self._date + other

    def __sub__(self, other):
        if isinstance(other, numbers.Number):
            return BasicDate(self._date - datetime.timedelta(days=float(other)))
        return self._date - other

    def __radd__(self, other):
        return other + self._date

    def __rsub__(self, other):
        return other - self._date

    def __repr__(self):
        return f"BasicDate('{self.__str__()}')"

    def __eq__(self, other):
        return type(other) == BasicDate and self._date == other._date

    def __hash__(self):
        return hash(self._date)

    def __lt__(self, other):
        return self.__str__('%Y%m%d') < BasicDate(other._date).__str__('%Y%m%d')

    def __gt__(self, other):
        return self.__str__('%Y%m%d') > BasicDate(other._date).__str__('%Y%m%d')

    def __le__(self, other):
        return self.__str__('%Y%m%d') <= BasicDate(other._date).__str__('%Y%m%d')

    def __ge__(self, other):
        return self.__str__('%Y%m%d') >= BasicDate(other._date).__str__('%Y%m%d')

    @property
    def date(self):
        return self._date

    def isocalendar(self):
        return self._date.isocalendar()


class BasicDateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            o = BasicDate(o)
        if isinstance(o, BasicDate):
            return {
                       "_type": "BasicDate",
                       "value": o.__format__('%Y%m%d')
                   }
        return super().default(o)


class BasicDateDecoder(JSONDecoder):
    def __init__(self, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        super().__init__(object_hook=self.object_hook, parse_float=parse_float, parse_int=parse_int,
                         parse_constant=parse_constant, strict=strict, object_pairs_hook=object_pairs_hook)

    def object_hook(self, obj):
        t = obj.get('_type', None)
        if t == 'BasicDate':
            return BasicDate(obj['value'], date_formats=['%Y%m%d'])
        return obj
