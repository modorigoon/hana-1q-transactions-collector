# -*- coding: utf-8 -*-
"""
    Datetime util
    author: modorigoon
    since: 0.1.0
"""
import datetime


def datetime_sequence_to_datetime(sequence):
    """ convert date time sequence to datetime object
    :param sequence: date time sequence
    :return: DATETIME
    """
    if len(sequence) != 14:
        return None
    return datetime.datetime.strptime(str(sequence), '%Y%m%d%H%M%S')


def datetime_to_sequence(date_time: datetime, return_time_unit=None):
    """ convert date time to date time sequence
    :param date_time: DATETIME object
    :param return_time_unit: sequence unit
    :return: date time sequence
    """
    _format = None
    if str(return_time_unit).lower() == 'date':
        _format = '%Y%m%d'
    elif str(return_time_unit).lower() == 'hour':
        _format = '%Y%m%d%H'
    elif str(return_time_unit).lower() == 'minute':
        _format = '%Y%m%d%H%M'
    elif str(return_time_unit).lower() == 'second':
        _format = '%Y%m%d%H%M%S'
    if _format is not None:
        return date_time.strftime(_format)
    return None
