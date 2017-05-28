# -*- coding: utf-8 -*-
"""Calculate the KPIs and the latest index required by the magic formula

The script calculate the KPIs and the latest index required by the
magic formula and store them into the database, so such data can be used
in the following steps for choosing stocks

"""


import pandas as pd
import numpy as np
from django.db.models import Q

from finance_report.models import (
    Stock, ChinaBalanceSheet, ChinaIncomeStatement)


def cal_china_data():
    """Calculate the data for the chinese market
    """

    # Load stock information from the database
    # Magic formula does not handle the following industries
    for stock in Stock.objects.exclude(
            Q(industry__exact='电力行业') |
            Q(industry__exact='公路桥梁') |
            Q(industry__exact='交通运输') |
            Q(industry__exact='金融行业') |
            Q(industry__exact='供水供气') |
            Q(industry__isnull=True)):

        balance_sheets = ChinaBalanceSheet.objects.filter(stock=stock)
        income_statements = ChinaIncomeStatement.objects.filter(stock=stock)

        balance_sheets_df = (pd.DataFrame(list(balance_sheets.values()))
                             .set_index('report_date')
                             .sort_index())
        income_statements_df = (pd.DataFrame(list(income_statements.values()))
                                .set_index('report_date')
                                .sort_index())

        # Calculate roce

        # For balance sheet related data, we need quarterly moving average
        magic_formula_df = (balance_sheets_df
                            .assign(excess_cash=lambda d:
                                np.maximum(
                                    0.0,
                                    (d['cash'] + d['trading_financial_assets'])
                                    - np.maximum(0.0, d['current_liabilities']
                                                 - (d['current_assets']
                                                    - (d['cash'] + d['trading_financial_assets'])))))
                            .assign(capital_employed=lambda d:
                                d['current_assets'] - d['current_liabilities']
                                - d['excess_cash'] + d['short_term_borrowings']
                                + d['notes_payable'] + d['non_current_liabilities_due']
                                + d['fixed_assets_net_value'] + d['investment_real_estates'])
                            )[['excess_cash', 'capital_employed']]
        magic_formula_df.loc[:, 'capital_employed_ma'] \
            = magic_formula_df['capital_employed'].rolling(center=False, window=4).mean()

        # For income statement related data, we need trailing twelve months

    print(magic_formula_df)
