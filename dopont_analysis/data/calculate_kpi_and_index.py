# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import datetime
from django.db.models import Q

from misc_helper.data import cal_trailing_year_series
from finance_report.models import (
    Stock, ChinaBalanceSheet, ChinaIncomeStatement)
from magic_formula.models import (LatestIndex, HistoricalKpi)


def cal_china_data():
    """Calculate the data for the chinese market
    """

    for stock in Stock.objects.filter(
            Q(stock_code__endswith='.sh')
            | Q(stock_code__endswith='.sz')):

        balance_sheets = ChinaBalanceSheet.objects.filter(
            stock=stock,
            report_date__gt=datetime.date(2006, 1, 1))
        income_statements = ChinaIncomeStatement.objects.filter(
            stock=stock,
            report_date__gt=datetime.date(2006, 1, 1))

        balance_sheets_df = (pd.DataFrame(list(balance_sheets.values()))
                               .set_index('report_date')
                               .sort_index())
        income_statements_df = (pd.DataFrame(list(income_statements.values()))
                                  .set_index('report_date')
                                  .sort_index())

        dopont_df = balance_sheets_df[['total_shareholders_equity', 'total_assets']]
