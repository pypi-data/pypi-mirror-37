# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

import datetime
import math

from decimal import Decimal
from . import constants, util

class attotimedelta(object):
    def __init__(self, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, nanoseconds=0):
        #Convert everything to nanoseconds
        total_nanoseconds = self._as_nanoseconds(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks, nanoseconds=nanoseconds)

        results_tuple = self._reduce_nanoseconds(total_nanoseconds)

        days = results_tuple[0]
        seconds = results_tuple[1]
        microseconds = results_tuple[2]
        milliseconds = results_tuple[3]
        minutes = results_tuple[4]
        hours = results_tuple[5]
        weeks = results_tuple[6]
        nanosesconds = results_tuple[7]

        #Create the native timedelta
        self._native_timedelta = datetime.timedelta(days=days, seconds=seconds, microseconds=microseconds, milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks)

        #Store the nanoseconds
        self._nanoseconds = Decimal(nanosesconds)

    @property
    def days(self):
        return self._native_timedelta.days

    @property
    def seconds(self):
        return self._native_timedelta.seconds

    @property
    def microseconds(self):
        return self._native_timedelta.microseconds

    @property
    def nanoseconds(self):
        return self._nanoseconds

    def __add__(self, y):
        #Return the result of x + y, where self is x
        x_nanoseconds = self.total_nanoseconds()
        y_nanoseconds = y.total_nanoseconds()

        result_tuple = self._reduce_nanoseconds(x_nanoseconds + y_nanoseconds)

        return attotimedelta(days=result_tuple[0], seconds=result_tuple[1], microseconds=result_tuple[2], milliseconds=result_tuple[3], minutes=result_tuple[4], hours=result_tuple[5], weeks=result_tuple[6], nanoseconds=result_tuple[7])

    def __sub__(self, y):
        #Return the result of x - y, where self is x
        return self + -y

    def __mul__(self, y):
        #Return the result of x * y, where self is x and y is an integer, float, or Decimal
        x_nanoseconds = self.total_nanoseconds()

        result_tuple = self._reduce_nanoseconds(x_nanoseconds * Decimal(y))

        return attotimedelta(days=result_tuple[0], seconds=result_tuple[1], microseconds=result_tuple[2], milliseconds=result_tuple[3], minutes=result_tuple[4], hours=result_tuple[5], weeks=result_tuple[6], nanoseconds=result_tuple[7])

    def __rmul__(self, y):
        #Return the result of y * x, where self ix x and y is an integer, float, or Decimal
        return self.__mul__(y)

    def __div__(self, y):
        #Return the result of x / y, where self is x and y is an integer, float, or Decimal
        x_nanoseconds = self.total_nanoseconds()

        result_tuple = self._reduce_nanoseconds(x_nanoseconds / Decimal(y))

        return attotimedelta(days=result_tuple[0], seconds=result_tuple[1], microseconds=result_tuple[2], milliseconds=result_tuple[3], minutes=result_tuple[4], hours=result_tuple[5], weeks=result_tuple[6], nanoseconds=result_tuple[7])

    def __truediv__(self, y):
        #Python3 division
        return self.__div__(y)

    def __floordiv__(self, y):
        #Return the result of x // y, where self is x and y is an integer, float, or Decimal
        x_nanoseconds = self.total_nanoseconds()

        result_tuple = self._reduce_nanoseconds(x_nanoseconds // Decimal(y))

        return attotimedelta(days=result_tuple[0], seconds=result_tuple[1], microseconds=result_tuple[2], milliseconds=result_tuple[3], minutes=result_tuple[4], hours=result_tuple[5], weeks=result_tuple[6], nanoseconds=result_tuple[7])

    def __eq__(self, y):
        #Return the result of x == y, where self is x
        if isinstance(y, self.__class__):
            return self.total_nanoseconds() == y.total_nanoseconds()

        #Other class doesn't match
        return False

    def __ne__(self, y):
        #Return the result of x != y, where self is x
        return not self.__eq__(y)

    def __gt__(self, y):
        #Return the result of x > y, where self is x
        if isinstance(y, self.__class__):
            return self.total_nanoseconds() > y.total_nanoseconds()
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __ge__(self, y):
        #Return the result of x >= y, where self is x
        if isinstance(y, self.__class__):
            return self.total_nanoseconds() >= y.total_nanoseconds()
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __lt__(self, y):
        #Return the result of x < y, where self is x
        if isinstance(y, self.__class__):
            return self.total_nanoseconds() < y.total_nanoseconds()
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __le__(self, y):
        #Return the result of x <= y, where self is x
        if isinstance(y, self.__class__):
            return self.total_nanoseconds() <= y.total_nanoseconds()
        else:
            raise TypeError('can\'t compare {0} to {1}'.format(type(self).__name__, type(y).__name__))

    def __pos__(self):
        #Return the result of +x, where self is x
        #
        #https://stackoverflow.com/questions/16819023/whats-the-purpose-of-the-pos-unary-operator-in-python
        return attotimedelta(nanoseconds=+self.total_nanoseconds())

    def __neg__(self):
        #Return the result of -x, where self is x
        return attotimedelta(nanoseconds=-self.total_nanoseconds())

    def __abs__(self):
        #Return the result of abs(x), where self is x
        return attotimedelta(nanoseconds=abs(self.total_nanoseconds()))

    def __str__(self):
        #Returns a string in the form [D day[s], ][H]H:MM:SS[.UUUUUU], where D is negative for negative t.
        nanoseconds = self.total_nanoseconds()

        reduced_tuple = self._reduce_nanoseconds(nanoseconds)

        if nanoseconds < 0:
            if reduced_tuple[1] != 0 or reduced_tuple[2] != 0 or reduced_tuple[3] != 0 or reduced_tuple[4] != 0 or reduced_tuple[5] != 0 or reduced_tuple[7] != 0:
                #We go to a negative day, then count forward
                days = -(abs(reduced_tuple[0]) + abs(reduced_tuple[6]) * constants.DAYS_PER_WEEK + 1)
            else:
                days = -(abs(reduced_tuple[0]) + abs(reduced_tuple[6]) * constants.DAYS_PER_WEEK)

            seconds = abs(reduced_tuple[1])
            microseconds = abs(reduced_tuple[2])
            milliseconds = abs(reduced_tuple[3])
            minutes = abs(reduced_tuple[4])
            hours = abs(reduced_tuple[5])
            nanoseconds = abs(reduced_tuple[7])

            #Now count forward
            remaining_nanoseconds = constants.NANOSECONDS_PER_DAY - (seconds * constants.NANOSECONDS_PER_SECOND + microseconds * constants.NANOSECONDS_PER_MICROSECOND + milliseconds * constants.NANOSECONDS_PER_MILLISECOND + minutes * constants.NANOSECONDS_PER_MINUTE + hours * constants.NANOSECONDS_PER_HOUR + nanoseconds)

            reduced_tuple = self._reduce_nanoseconds(remaining_nanoseconds)

            seconds = reduced_tuple[1]
            microseconds = reduced_tuple[2]
            milliseconds = reduced_tuple[3]
            minutes = reduced_tuple[4]
            hours = reduced_tuple[5]
            nanoseconds = reduced_tuple[7]
        else:
            days = reduced_tuple[0] + reduced_tuple[6] * constants.DAYS_PER_WEEK
            seconds = reduced_tuple[1]
            microseconds = reduced_tuple[2]
            milliseconds = reduced_tuple[3]
            minutes = reduced_tuple[4]
            hours = reduced_tuple[5]
            nanoseconds = reduced_tuple[7]

        #Combine the seconds
        combined_seconds = seconds + (microseconds / constants.MICROSECONDS_PER_SECOND) + (milliseconds / constants.MILLISECONDS_PER_SECOND) + (nanoseconds / constants.NANOSECONDS_PER_SECOND)

        #Build the strings
        if days == 0:
            days_str = ''
        elif abs(days) > 1:
            days_str = str(days) + ' days'
        else:
            days_str = str(days) + ' day'

        if combined_seconds == 0:
            time_str = str(hours) + ':' + '{0:02d}'.format(minutes) + ':00'
        elif combined_seconds < 10:
            time_str = str(hours) + ':' + '{0:02d}'.format(minutes) + ':0' + util.decimal_stringify(combined_seconds)
        else:
            time_str = str(hours) + ':' + '{0:02d}'.format(minutes) + ':' + util.decimal_stringify(combined_seconds)

        if days_str == '':
            return time_str
        else:
            return days_str + ', ' + time_str

    def __repr__(self):
        #Returns a string in the form attotime.timedelta(D[, S[, U[, N]]]), where D is negative for negative t
        nanoseconds = self.total_nanoseconds()

        reduced_tuple = self._reduce_nanoseconds(nanoseconds)

        if nanoseconds < 0:
            if reduced_tuple[1] != 0 or reduced_tuple[2] != 0 or reduced_tuple[3] != 0 or reduced_tuple[4] != 0 or reduced_tuple[5] != 0 or reduced_tuple[7] != 0:
                #We go to a negative day, then count forward
                days = -(abs(reduced_tuple[0]) + abs(reduced_tuple[6]) * constants.DAYS_PER_WEEK + 1)
            else:
                days = -(abs(reduced_tuple[0]) + abs(reduced_tuple[6]) * constants.DAYS_PER_WEEK)

            seconds = abs(reduced_tuple[1])
            microseconds = abs(reduced_tuple[2])
            milliseconds = abs(reduced_tuple[3])
            minutes = abs(reduced_tuple[4])
            hours = abs(reduced_tuple[5])
            nanoseconds = abs(reduced_tuple[7])

            #Now count forward
            remaining_nanoseconds = constants.NANOSECONDS_PER_DAY - (seconds * constants.NANOSECONDS_PER_SECOND + microseconds * constants.NANOSECONDS_PER_MICROSECOND + milliseconds * constants.NANOSECONDS_PER_MILLISECOND + minutes * constants.NANOSECONDS_PER_MINUTE + hours * constants.NANOSECONDS_PER_HOUR + nanoseconds)

            reduced_tuple = self._reduce_nanoseconds(remaining_nanoseconds)

            seconds = reduced_tuple[1]
            microseconds = reduced_tuple[2]
            milliseconds = reduced_tuple[3]
            minutes = reduced_tuple[4]
            hours = reduced_tuple[5]
            nanoseconds = reduced_tuple[7]
        else:
            days = reduced_tuple[0] + reduced_tuple[6] * constants.DAYS_PER_WEEK
            seconds = reduced_tuple[1]
            microseconds = reduced_tuple[2]
            milliseconds = reduced_tuple[3]
            minutes = reduced_tuple[4]
            hours = reduced_tuple[5]
            nanoseconds = reduced_tuple[7]

        combined_seconds = hours * constants.SECONDS_PER_HOUR + minutes * constants.SECONDS_PER_MINUTE + seconds
        combined_microseconds = milliseconds * constants.MICROSECONDS_PER_MILLISECOND + microseconds

        repr_string = self.__class__.__module__ + '(' + str(days)

        if combined_seconds != 0 or combined_microseconds != 0 or nanoseconds != 0:
            repr_string += (', ' + str(combined_seconds))

        if combined_microseconds != 0 or nanoseconds != 0:
            repr_string += (', ' + str(combined_microseconds))

        if nanoseconds != 0:
            repr_string += (', ' + util.decimal_stringify(nanoseconds))

        repr_string += ')'

        return repr_string

    def total_seconds(self):
        return self.total_nanoseconds() / constants.NANOSECONDS_PER_SECOND

    def total_nanoseconds(self):
        #Converts the entire timedelta to nanoseconds
        return self._as_nanoseconds(days=self._native_timedelta.days, seconds=self._native_timedelta.seconds, microseconds=self._native_timedelta.microseconds, nanoseconds=self._nanoseconds)

    @staticmethod
    def _as_nanoseconds(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0, nanoseconds=0):
        return Decimal(days) * constants.NANOSECONDS_PER_DAY + Decimal(seconds) * constants.NANOSECONDS_PER_SECOND + Decimal(microseconds) * constants.NANOSECONDS_PER_MICROSECOND + Decimal(milliseconds) * constants.NANOSECONDS_PER_MILLISECOND + Decimal(minutes) * constants.NANOSECONDS_PER_MINUTE + Decimal(hours) * constants.NANOSECONDS_PER_HOUR + Decimal(weeks) * constants.NANOSECONDS_PER_WEEK + Decimal(nanoseconds)

    @staticmethod
    def _reduce_nanoseconds(nanoseconds):
        return _reduce_to_tuple(nanoseconds, constants.NANOSECONDS_PER_WEEK, constants.NANOSECONDS_PER_DAY, constants.NANOSECONDS_PER_HOUR, constants.NANOSECONDS_PER_MINUTE, constants.NANOSECONDS_PER_SECOND, constants.NANOSECONDS_PER_MILLISECOND, constants.NANOSECONDS_PER_MICROSECOND, 1)

def _reduce_to_tuple(value, week_reduction, day_reduction, hour_reduction, minute_reduction, second_reduction, millisecond_reduction, microsecond_reduction, nanosecond_reduction):
    def _reduce(value, reduction):
        if reduction > 1 or reduction < 1:
            reduced_value, remainder = util.reduce(value, reduction)
        else:
            #The integer part is already of the type we're reducing
            remainder, reduced_value = util.decimal_split(value)

        return reduced_value, remainder

    remainder = abs(Decimal(value))

    reduced_weeks, remainder = _reduce(remainder, week_reduction)
    reduced_days, remainder = _reduce(remainder, day_reduction)
    reduced_hours, remainder = _reduce(remainder, hour_reduction)
    reduced_minutes, remainder = _reduce(remainder, minute_reduction)
    reduced_seconds, remainder = _reduce(remainder, second_reduction)
    reduced_milliseconds, remainder = _reduce(remainder, millisecond_reduction)
    reduced_microseconds, remainder = _reduce(remainder, microsecond_reduction)
    nanoseconds = remainder * nanosecond_reduction

    #Return the mess, ints for everything but nanoseconds
    return (
        int(math.copysign(reduced_days, value)),
        int(math.copysign(reduced_seconds, value)),
        int(math.copysign(reduced_microseconds, value)),
        int(math.copysign(reduced_milliseconds, value)),
        int(math.copysign(reduced_minutes, value)),
        int(math.copysign(reduced_hours, value)),
        int(math.copysign(reduced_weeks, value)),
        nanoseconds.copy_sign(Decimal(value)),
    )
