# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime

from decimal import Decimal
from . import constants, util

class attotime(object):
    def __init__(self, hour=0, minute=0, second=0, microsecond=0, nanosecond=0, tzinfo=None):
        #Everything is stored as an integer, except for nanoseconds, which is stored as a Decimal
        if nanosecond < 0 or nanosecond >= constants.NANOSECONDS_PER_MICROSECOND:
            raise ValueError('nanosecond must be in 0..{0}'.format(constants.NANOSECONDS_PER_MICROSECOND))

        #Create the native time object
        self._native_time = datetime.time(hour=hour, minute=minute, second=second, microsecond=microsecond)

        self._nanosecond = nanosecond

        self._tzinfo = tzinfo

    @property
    def hour(self):
        return self._native_time.hour

    @property
    def minute(self):
        return self._native_time.minute

    @property
    def second(self):
        return self._native_time.second

    @property
    def microsecond(self):
        return self._native_time.microsecond

    @property
    def nanosecond(self):
        return self._nanosecond

    @property
    def tzinfo(self):
        return self._tzinfo

    def replace(self, hour=None, minute=None, second=None, microsecond=None, nanosecond=None, tzinfo=True):
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
        #https://github.com/python/cpython/blob/master/Lib/datetime.py#L1315
        if tzinfo is True:
            tzinfo = self.tzinfo

        return attotime(hour=hour, minute=minute, second=second, microsecond=microsecond, nanosecond=nanosecond, tzinfo=tzinfo)

    def isoformat(self):
        #Returns a string of the form HH:MM:SS[.mmmmmm][+HH:MM]
        combined_seconds = self.second + (self.microsecond / constants.MICROSECONDS_PER_SECOND) + (self.nanosecond / constants.NANOSECONDS_PER_SECOND)

        if combined_seconds == 0:
            time_str = '{0:02d}:{1:02d}:00'.format(self.hour, self.minute)
        elif combined_seconds < 10:
            time_str = '{0:02d}:{1:02d}:0{2}'.format(self.hour, self.minute, util.decimal_stringify(combined_seconds))
        else:
            time_str = '{0:02d}:{1:02d}:{2}'.format(self.hour, self.minute, util.decimal_stringify(combined_seconds))

        if self.utcoffset() is not None:
            offset = self.utcoffset()

            if offset is not None:
                #Build a +HH:MM string
                if offset.days < 0:
                    sign_str = '-'
                    offset = -offset
                else:
                    sign_str = '+'

                offset_hours, remaining_seconds = util.reduce(Decimal(offset.total_seconds()), constants.SECONDS_PER_HOUR)
                offset_minutes, offset_seconds = util.reduce(remaining_seconds, constants.SECONDS_PER_MINUTE)

                if offset_seconds == 0:
                    offset_str = '{0}{1:02d}:{2:02d}'.format(sign_str, int(offset_hours), int(offset_minutes))
                else:
                    offset_str = '{0}{1:02d}:{2:02d}:{3:02d}'.format(sign_str, int(offset_hours), int(offset_minutes), int(offset_seconds))

                time_str += offset_str

        return time_str

    def strftime(self, formatstr):
        raise NotImplementedError

    def utcoffset(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.utcoffset(None)

    def dst(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.dst(None)

    def tzname(self):
        if self.tzinfo is None:
            return None

        return self.tzinfo.tzname(self.tzinfo)

    def __eq__(self, y):
        #Return the result of x == y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                #Do a naive comparison
                return self._native_time == y._native_time and self._nanosecond == y._nanosecond
            elif self.tzinfo is not None and y.tzinfo is not None:
                #Do a tz aware comparison, since there is currently not a nanosecond aware
                #tzinfo implementation, just compare each part separately
                return self._native_time.replace(tzinfo=self.tzinfo) == y._native_time.replace(tzinfo=y.tzinfo) and self._nanosecond == y._nanosecond
            else:
                raise TypeError('can\'t compare offset-naive and offset-aware times')

        return False

    def __ne__(self, y):
        #Return the result of x != y, where self is x
        return not self.__eq__(y)

    def __gt__(self, y):
        #Return the result of x > y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                #Do a naive comparison
                return (self._native_time > y._native_time) or (self._native_time == y._native_time and self._nanosecond > y._nanosecond)
            elif self.tzinfo is not None and y.tzinfo is not None:
                #Do a tz aware comparison, since there is currently not a nanosecond aware
                #tzinfo implementation, just compare each part separately
                return (self._native_time.replace(tzinfo=self.tzinfo) > y._native_time.replace(tzinfo=y.tzinfo) and self._nanosecond == y._nanosecond) or (self._native_time.replace(tzinfo=self.tzinfo) == y._native_time.replace(tzinfo=y.tzinfo) and self._nanosecond > y._nanosecond)
            else:
                raise TypeError('can\'t compare offset-naive and offset-aware times')
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __ge__(self, y):
        #Return the result of x >= y, where self is x
        if isinstance(y, self.__class__):
            return (self > y) or (self == y)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __lt__(self, y):
        #Return the result of x < y, where self is x
        if isinstance(y, self.__class__):
            if self.tzinfo is None and y.tzinfo is None:
                #Do a naive comparison
                return (self._native_time < y._native_time) or (self._native_time == y._native_time and self._nanosecond < y._nanosecond)
            elif self.tzinfo is not None and y.tzinfo is not None:
                #Do a tz aware comparison, since there is currently not a nanosecond aware
                #tzinfo implementation, just compare each part separately
                return (self._native_time.replace(tzinfo=self.tzinfo) < y._native_time.replace(tzinfo=y.tzinfo) and self._nanosecond == y._nanosecond) or (self._native_time.replace(tzinfo=self.tzinfo) == y._native_time.replace(tzinfo=y.tzinfo) and self._nanosecond < y._nanosecond)
            else:
                raise TypeError('can\'t compare offset-naive and offset-aware times')
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __le__(self, y):
        #Return the result of x <= y, where self is x
        if isinstance(y, self.__class__):
            return (self < y) or (self == y)
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __str__(self):
        return self.isoformat()

    def __repr__(self):
        if self._tzinfo is None:
            return '{0}({1}, {2}, {3}, {4}, {5})'.format(self.__class__.__module__, self.hour, self.minute, self.second, self.microsecond, str(self.nanosecond))

        return '{0}({1}, {2}, {3}, {4}, {5}, {6})'.format(self.__class__.__module__, self.hour, self.minute, self.second, self.microsecond, str(self.nanosecond), str(self._tzinfo))

    def __format__(self, formatstr):
        return self.strftime(formatstr)
