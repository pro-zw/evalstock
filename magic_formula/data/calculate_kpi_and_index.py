# -*- coding: utf-8 -*-
"""Calculate the KPIs and the latest index required by the magic formula

The script calculate the KPIs and the latest index required by the
magic formula and store them into the database, so such data can be used
in the following steps for choosing stocks

"""


import pandas as pd
import numpy as np
import datetime
from django.db.models import Q

from finance_report.models import (
    Stock, ChinaBalanceSheet, ChinaIncomeStatement, ChinaCashFlowStatement)
from magic_formula.models import (
    LatestIndex, HistoricalKpi)


def cal_china_data():
    """Calculate the data for the chinese market
    """

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

    # Load stock information from the database
    # Magic formula does not handle the following industries
    for stock in Stock.objects.exclude(
            Q(industry__exact='电力行业') |
            Q(industry__exact='公路桥梁') |
            Q(industry__exact='交通运输') |
            Q(industry__exact='金融行业') |
            Q(industry__exact='供水供气') |
            Q(industry__isnull=True)):

        balance_sheets = ChinaBalanceSheet.objects.filter(
            stock=stock,
            report_date__gt=datetime.date(2006, 1, 1))
        income_statements = ChinaIncomeStatement.objects.filter(
            stock=stock,
            report_date__gt=datetime.date(2006, 1, 1))
        cashflow_statements = ChinaCashFlowStatement.objects.filter(
            stock=stock,
            report_date__gt=datetime.date(2006, 1, 1))

        balance_sheets_df = (pd.DataFrame(list(balance_sheets.values()))
                             .set_index('report_date')
                             .sort_index())
        income_statements_df = (pd.DataFrame(list(income_statements.values()))
                                .set_index('report_date')
                                .sort_index())
        cashflow_statements_df = (pd.DataFrame(list(cashflow_statements.values()))
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
        magic_formula_df.loc[:, 'capital_employed_mean'] \
            = magic_formula_df['capital_employed'].rolling(center=False, window=5).mean()

        # For income statement related data, we need difference of trailing twelve months
        magic_formula_df.loc[:, 'ebit_without_joint'] = (
            income_statements_df.assign(ebit_without_joint=lambda d:
                                        d['operations_income'] - d['operations_costs']
                                        - d['taxes_and_surcharges']
                                        - d['admin_expenses']
                                        - d['selling_expenses'])
            )['ebit_without_joint']

        magic_formula_df.loc[:, 'ebit_with_joint'] = (
            income_statements_df.assign(ebit_with_joint=lambda d:
                                        d['operations_income'] - d['operations_costs']
                                        - d['taxes_and_surcharges']
                                        - d['admin_expenses']
                                        - d['selling_expenses']
                                        + d['income_from_joint'])
            )['ebit_with_joint']

        magic_formula_df.loc[:, 'ebit_without_joint_ttm'] = cal_trailing_year_series(
            magic_formula_df['ebit_without_joint']
        )

        magic_formula_df.loc[:, 'ebit_with_joint_ttm'] = cal_trailing_year_series(
            magic_formula_df['ebit_with_joint']
        )

        magic_formula_df.loc[:, 'roce'] = magic_formula_df['ebit_without_joint'] \
            / magic_formula_df['capital_employed_mean']

        magic_formula_df.loc[:, 'roce_ttm'] = magic_formula_df['ebit_without_joint_ttm'] \
            / magic_formula_df['capital_employed_mean']

        # Calculate net profit reality
        magic_formula_df.loc[:, 'net_profit_reality'] = \
            cashflow_statements_df['net_cash_flows_from_operating_activities'] \
            / income_statements_df['net_profit']

        # Calculate earning yield
        latest_balance_sheet = balance_sheets_df.tail(1)
        latest_ebit_with_joint_ttm = magic_formula_df['ebit_with_joint_ttm'].iloc[-1]
        latest_excess_cash = magic_formula_df['excess_cash'].iloc[-1]

        earnings_yield = (latest_ebit_with_joint_ttm
                          / (stock.market_value
                             + latest_balance_sheet['short_term_borrowings']
                             + latest_balance_sheet['notes_payable']
                             + latest_balance_sheet['non_current_liabilities_due']
                             + latest_balance_sheet['long_term_borrowings']
                             + latest_balance_sheet['debt_securities_issued']
                             + latest_balance_sheet['minority_shareholders_equity']
                             - latest_balance_sheet['available_for_sale_financial_assets']
                             - latest_balance_sheet['held_to_maturity_investments']
                             + latest_balance_sheet['deferred_tax_liabilities']
                             - latest_excess_cash
                             )
                          )

        magic_formula_df = magic_formula_df.dropna().sort_index()

        # Save all results into the database
        latest_magic_formula_index = magic_formula_df.tail(1)
        latest_index, _ = LatestIndex.objects.update_or_create(
            stock=stock,
            defaults={
                'ebit_without_joint': latest_magic_formula_index['ebit_without_joint'],
                'ebit_without_joint_ttm': latest_magic_formula_index['ebit_without_joint_ttm'],
                'ebit_with_joint': latest_magic_formula_index['ebit_with_joint'],
                'ebit_with_joint_ttm': latest_magic_formula_index['ebit_with_joint_ttm'],
                'roce': latest_magic_formula_index['roce'],
                'roce_ttm': latest_magic_formula_index['roce_ttm'],
                'earnings_yield': earnings_yield,
                'net_profit_reality': latest_magic_formula_index['net_profit_reality'],
            })
        latest_index.save()

        for row in magic_formula_df.iterrows():
            historical_kpi, _ = HistoricalKpi.objects.update_or_create(
                stock=stock, report_date=row[0],
                defaults={
                    'ebit_without_joint': row[1]['ebit_without_joint'],
                    'ebit_without_joint_ttm': row[1]['ebit_without_joint_ttm'],
                    'ebit_with_joint': row[1]['ebit_with_joint'],
                    'ebit_with_joint_ttm': row[1]['ebit_with_joint_ttm'],
                    'roce': row[1]['roce'],
                    'roce_ttm': row[1]['roce_ttm'],
                    'net_profit_reality': row[1]['net_profit_reality'],
                })
            historical_kpi.save()
