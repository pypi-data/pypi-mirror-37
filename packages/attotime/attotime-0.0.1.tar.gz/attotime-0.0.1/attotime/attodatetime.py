# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from . import constants, util
from .attotime import attotime
from .attotimedelta import attotimedelta

class attodatetime(object):
    def __init__(self, year, month, day, hour=0, minute=0, second=0, microsecond=0, nanosecond=0, tzinfo=None):
        #Create the native date object
        self._native_date = datetime.date(year=year, month=month, day=day)

        #Create the attotime time object
        self._attotime = attotime(hour=hour, minute=minute, second=second, microsecond=microsecond, nanosecond=nanosecond, tzinfo=tzinfo)

    @classmethod
    def today(cls):
        raise NotImplementedError

    @classmethod
    def now(cls, tz=None):
        raise NotImplementedError

    @classmethod
    def utcnow(cls):
        raise NotImplementedError

    @classmethod
    def fromtimestamp(cls, timestamp, tz=None):
        raise NotImplementedError

    @classmethod
    def utcfromtimestamp(cls, timestamp):
        raise NotImplementedError

    @classmethod
    def fromordinal(cls, ordinal):
        date = datetime.datetime.fromordinal(ordinal)

        return cls(year=date.year, month=date.month, day=date.day)

    @classmethod
    def combine(cls, date, time):
        result = cls(year=1, month=1, day=1)

        #Now replace the instance objects
        result._native_date = datetime.date(year=date.year, month=date.month, day=date.day)
        result._attotime = time

        return result

    @classmethod
    def strptime(cls, date_string, format):
        raise NotImplementedError

    @property
    def year(self):
        return self._native_date.year

    @property
    def month(self):
        return self._native_date.month

    @property
    def day(self):
        return self._native_date.day

    @property
    def hour(self):
        return self._attotime.hour

    @property
    def minute(self):
        return self._attotime.minute

    @property
    def second(self):
        return self._attotime.second

    @property
    def microsecond(self):
        return self._attotime.microsecond

    @property
    def nanosecond(self):
        return self._attotime.nanosecond

    @property
    def tzinfo(self):
        return self._attotime.tzinfo

    def date(self):
        return self._as_datetime().date()

    def time(self):
        return attotime(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, nanosecond=self.nanosecond)

    def timetz(self):
        return attotime(hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, nanosecond=self.nanosecond, tzinfo=self.tzinfo)

    def replace(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, nanosecond=None, tzinfo=True):
        if year is None:
            year = self.year

        if month is None:
            month = self.month

        if day is None:
            day = self.day

        if hour is None:
            hour = self.hour

        if minute is None:
            minute = self.minute

        if second is None:
            second = self.second

        if microsecond is None:
            microsecond = self.microsecond

        if nanosecond is None:
            nanosecond = self.nanosecond

        #Use True to support clearing tzinfo by setting tzinfo=None
        #https://github.com/python/cpython/blob/master/Lib/datetime.py#L1596
        if tzinfo is True:
            tzinfo = self.tzinfo

        return attodatetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond, nanosecond=nanosecond, tzinfo=tzinfo)

    def astimezone(self, tz):
        raise NotImplementedError

    def utcoffset(self):
        #Offsets don't have nanosecond resolution, so build a native datetime
        native_datetime = self._as_datetime()

        native_timedelta = native_datetime.utcoffset()

        if native_timedelta is None:
            return None

        #Convert the native timedelta to an attotimedelta
        return attotimedelta(days=native_timedelta.days, seconds=native_timedelta.seconds, microseconds=native_timedelta.microseconds, nanoseconds=0)

    def dst(self):
        if self.tzinfo is None:
            return None

        #Offsets don't have nanosecond resolution, so build a native datetime
        native_datetime = self._as_datetime()

        native_timedelta = native_datetime.tzinfo.dst(native_datetime)

        #Convert the native timedelta to an attotimedelta
        return attotimedelta(days=native_timedelta.days, seconds=native_timedelta.seconds, microseconds=native_timedelta.microseconds, nanoseconds=0)

    def tzname(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.tzname(self.tzinfo)

    def timetuple(self):
        return self._as_datetime().timetuple()

    def utctimetuple(self):
        return self._as_datetime().utctimetuple()

    def toordinal(self):
        return self._as_datetime().toordinal()

    def weekday(self):
        return self._as_datetime().weekday()

    def isoweekday(self):
        return self._as_datetime().isoweekday()

    def isocalendar(self):
        return self._as_datetime().isocalendar()

    def isoformat(self, separator='T'):
        return separator.join([self._as_datetime().date().isoformat(), self._attotime.isoformat()])

    def ctime(self):
        return self._as_datetime().ctime()

    def strftime(self, formatstr):
        raise NotImplementedError

    def __add__(self, y):
        #Return the result of x + y, where self is x and y is an attotimedelta
        if not isinstance(y, attotimedelta):
            return NotImplemented

        delta = attotimedelta(days=self._native_date.toordinal(), hours=self.hour, minutes=self.minute, seconds=self.second, microseconds=self.microsecond, nanoseconds=self.nanosecond)

        delta += y

        hour, remaining_seconds = util.reduce(delta.seconds, constants.SECONDS_PER_HOUR)
        minute, second = util.reduce(remaining_seconds, constants.SECONDS_PER_MINUTE)

        if delta.days > 0 and delta.days < datetime.date.max.toordinal():
            return self.combine(datetime.date.fromordinal(delta.days), attotime(hour, minute, second, delta.microseconds, delta.nanoseconds, tzinfo=self.tzinfo))

        raise OverflowError('result out of range')

    def __sub__(self, y):
        #Returns the result of x - y, where self ix x, and y is
        #an attodatetime or attotimedelta, when y is an attodatetime,
        #the result is an attotimedelta, when y is an attotimedelta,
        #the result is an attodatetime
        if not isinstance(y, attodatetime):
            if isinstance(y, attotimedelta):
                #y is an attotimedelta
                return self + -y

            return NotImplemented

        #y is an attodatetime, build an attotimedelta
        daysx = self._native_date.toordinal()
        daysy = y._native_date.toordinal()

        secondsx = self.second + self.minute * constants.SECONDS_PER_MINUTE + self.hour * constants.SECONDS_PER_HOUR
        secondsy = y.second + y.minute * constants.SECONDS_PER_MINUTE + y.hour * constants.SECONDS_PER_HOUR

        microsecondsx = self.microsecond
        microsecondsy = y.microsecond

        nanosecondsx = self.nanosecond
        nanosecondsy = y.nanosecond

        base = attotimedelta(days=daysx - daysy, seconds=secondsx - secondsy, microseconds=microsecondsx - microsecondsy, nanoseconds=nanosecondsx-nanosecondsy)

        if self.tzinfo is y.tzinfo:
            return base

        offsetx = self.utcoffset()
        offsety = y.utcoffset()

        if offsetx == offsety:
            return base

        if offsetx is None or offsety is None:
            raise TypeError('cannot mix naive and timezone-aware time')

        return base + offsety - offsetx

    def __eq__(self, y):
        #Return the result of x == y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date == y._native_date and self._attotime == y._attotime

        return False

    def __ne__(self, y):
        #Return the result of x != y, where self is x
        return not self.__eq__(y)

    def __gt__(self, y):
        #Return the result of x > y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date > y._native_date or (self._native_date == y._native_date and self._attotime > y._attotime)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __ge__(self, y):
        #Return the result of x >= y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date > y._native_date or (self._native_date == y._native_date and self._attotime >= y._attotime)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __lt__(self, y):
        #Return the result of x < y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date < y._native_date or (self._native_date == y._native_date and self._attotime < y._attotime)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __le__(self, y):
        #Return the result of x <= y, where self is x
        if isinstance(y, self.__class__):
            return self._native_date < y._native_date or (self._native_date == y._native_date and self._attotime <= y._attotime)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __str__(self):
        return self.isoformat(separator=' ')

    def __repr__(self):
        if self._attotime.tzinfo is None:
            return '{0}({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})'.format(self.__class__.__module__, self._native_date.year, self._native_date.month, self._native_date.day, self._attotime.hour, self._attotime.minute, self._attotime.second, self._attotime.microsecond, str(self._attotime.nanosecond))

        return '{0}({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})'.format(self.__class__.__module__, self._native_date.year, self._native_date.month, self._native_date.day, self._attotime.hour, self._attotime.minute, self._attotime.second, self._attotime.microsecond, str(self._attotime.nanosecond), str(self._attotime.tzinfo))

    def __format__(self, formatstr):
        return self.strftime(formatstr)

    def _as_datetime(self):
        #Returns the attodatetime as a native datetime, losing nanosecond resolution
        return datetime.datetime(year=self.year, month=self.month, day=self.day, hour=self.hour, minute=self.minute, second=self.second, microsecond=self.microsecond, tzinfo=self.tzinfo)
