# -*- coding: utf-8 -*-

# Copyright (c) 2018, Brandon Nielsen
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the BSD license.  See the LICENSE file for details.

from aniso8601.builder import BaseTimeBuilder, PythonTimeBuilder

class RelativeValueError(ValueError):
    """Raised when an invalid value is given for calendar level accuracy."""

class RelativeTimeBuilder(PythonTimeBuilder):
    @classmethod
    def build_duration(cls, PnY=None, PnM=None, PnW=None, PnD=None, TnH=None,
                       TnM=None, TnS=None):

        try:
            import dateutil.relativedelta
        except ImportError:
            raise RuntimeError('dateutil must be installed for '
                               'relativedelta support.')

        if ((PnY is not None and '.' in PnY)
                or (PnM is not None and '.' in PnM)):
            #https://github.com/dateutil/dateutil/issues/40
            raise RelativeValueError('Fractional months and years are not '
                                     'defined for relative durations.')

        years = 0
        months = 0
        days = 0
        weeks = 0
        hours = 0
        minutes = 0
        seconds = 0
        microseconds = 0

        if PnY is not None:
            years = BaseTimeBuilder.cast(PnY,
                                         int,
                                         thrownmessage=
                                         'Invalid year string.')

        if PnM is not None:
            months = BaseTimeBuilder.cast(PnM,
                                          int,
                                          thrownmessage=
                                          'Invalid month string.')

        if PnD is not None:
            days = BaseTimeBuilder.cast(PnD,
                                        float,
                                        thrownmessage=
                                        'Invalid day string.')

        if PnW is not None:
            if '.' in PnW:
                weeks = BaseTimeBuilder.cast(PnW,
                                             float,
                                             thrownmessage=
                                             'Invalid week string.')
            else:
                weeks = BaseTimeBuilder.cast(PnW,
                                             int,
                                             thrownmessage=
                                             'Invalid week string.')

        if TnH is not None:
            if '.' in TnH:
                hours = BaseTimeBuilder.cast(TnH,
                                             float,
                                             thrownmessage=
                                             'Invalid hour string.')
            else:
                hours = BaseTimeBuilder.cast(TnH,
                                             int,
                                             thrownmessage=
                                             'Invalid hour string.')

        if TnM is not None:
            if '.' in TnM:
                minutes = BaseTimeBuilder.cast(TnM,
                                               float,
                                               thrownmessage=
                                               'Invalid minute string.')
            else:
                minutes = BaseTimeBuilder.cast(TnM,
                                               int,
                                               thrownmessage=
                                               'Invalid minute string.')

        if TnS is not None:
            if '.' in TnS:
                #Split into seconds and microseconds
                seconds = BaseTimeBuilder.cast(TnS[0:TnS.index('.')],
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

                #Truncate to maximum supported precision
                microseconds = (BaseTimeBuilder.cast(TnS[TnS.index('.'):
                                                         TnS.index('.') + 7],
                                                     float,
                                                     thrownmessage=
                                                     'Invalid second string.')
                                * 1e6)
            else:
                seconds = BaseTimeBuilder.cast(TnS,
                                               int,
                                               thrownmessage=
                                               'Invalid second string.')

        return dateutil.relativedelta.relativedelta(years=years,
                                                    months=months,
                                                    weeks=weeks,
                                                    days=days,
                                                    hours=hours,
                                                    minutes=minutes,
                                                    seconds=seconds,
                                                    microseconds=microseconds)
