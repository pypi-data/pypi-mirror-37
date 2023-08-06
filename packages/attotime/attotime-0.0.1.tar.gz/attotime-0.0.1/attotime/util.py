# Copyright (c) 2016, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from decimal import getcontext

def tuple_add(a, b):
    #http://stackoverflow.com/questions/497885/python-element-wise-tuple-operations-like-sum
    return tuple([item1 + item2 for item1, item2 in zip(a, b)])

def reduce(value, reduction):
    #Given a value and a reduction, returns a tuple containing the reduced value
    #and the remainder, the reduced value is the number of complete reductions
    #that fit into the value, the remainder is whatever is left.
    #Both are returned as Decimal
    #
    #Examples:
    #   reduce(5, 2) = (Decimal(2), Decimal(1))
    #   reduce(6, 2) = (Decimal(3), Decimal(0))
    #   reduce(2, 2) = (Decimal(1), Decimal(0))
    #   reduce(1, 2) = (Decimal(0), Decimal(1))
    reduced_value, remainder = getcontext().divmod(value, reduction)

    return (reduced_value, remainder)

def decimal_split(decimal):
    #Splits a Decimal object into fractional and integer parts, returned as Decimal
    integer_part, fractional_part = getcontext().divmod(decimal, 1)

    return (fractional_part, integer_part)

def decimal_stringify(decimal):
    #https://stackoverflow.com/questions/11227620/drop-trailing-zeros-from-decimal
    decimal_string = str(decimal)

    if 'E' in decimal_string:
        #Arbitrarily force 16 place fixed point
        decimal_string = '{0:16f}'.format(decimal)

    if '.' in decimal_string:
        decimal_string = decimal_string.rstrip('0').rstrip('.')

    return decimal_string.strip()
