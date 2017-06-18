# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime


def find_trailing_year_dates(end_date: datetime.date) -> tuple:
    """Find the related financial report dates to calculate
    Trailing Twelve Months (TTM) data

    :param end_date: The date begins
    :return: Return the tuple which contains three dates
    (begin_date, annual report date, and the end date). If
    the end_date is annual report date, return the tuple which
    contains only this date immediately

    """

    if end_date.month == 12:
        return end_date,

    return (datetime.date(end_date.year - 1, end_date.month, end_date.day),
            datetime.date(end_date.year - 1, 12, 31),
            end_date)


def cal_trailing_year_series(input_series: pd.Series) -> pd.Series:
    """Calculate the trailing year series based on the original series data

    :param input_series: The original data
    :return: The trailing year series calculated

    """

    result_dict = {}
    for report_date, value in input_series.iteritems():
        ttm_dates = find_trailing_year_dates(report_date)
        if len(ttm_dates) == 1:
            result_dict[report_date] = input_series[report_date]
        else:
            begin_date, annual_report_date, end_date = ttm_dates
            if (begin_date in input_series.index
                    and annual_report_date in input_series.index):

                result_dict[report_date] = (input_series[annual_report_date]
                                            - input_series[begin_date]
                                            + input_series[end_date])
            else:
                result_dict[report_date] = np.nan

    return pd.Series(result_dict)
