# -*- coding: utf-8 -*-

import pandas as pd
import datetime
from django.db.models import Q

from misc_helper.data import cal_trailing_year_series
from finance_report.models import (
    Stock, ChinaBalanceSheet, ChinaIncomeStatement)
from dopont_analysis.models import (LatestIndex, HistoricalKpi)


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

        if len(balance_sheets) == 0 or len(income_statements) == 0:
            continue

        balance_sheets_df = (pd.DataFrame(list(balance_sheets.values()))
                               .set_index('report_date')
                               .sort_index())
        income_statements_df = (pd.DataFrame(list(income_statements.values()))
                                  .set_index('report_date')
                                  .sort_index())

        operations_income_ttm_series = \
            cal_trailing_year_series(income_statements_df['operations_income'])
        operations_costs_ttm_series = \
            cal_trailing_year_series(income_statements_df['operations_costs'])
        net_profit_ttm_series = \
            cal_trailing_year_series(income_statements_df['net_profit'])
        total_assets_mean = \
            balance_sheets_df['total_assets'].rolling(center=False, window=4).mean()
        total_shareholders_equity_mean = \
            balance_sheets_df['total_shareholders_equity'].rolling(center=False, window=4).mean()

        dopont_df = pd.DataFrame(index=income_statements_df.index.copy())

        dopont_df.loc[:, 'gross_margin'] = \
            (income_statements_df['operations_income']
             - income_statements_df['operations_costs']) \
            / income_statements_df['operations_income']
        dopont_df.loc[:, 'gross_margin_ttm'] = \
            (operations_income_ttm_series
             - operations_costs_ttm_series) \
            / operations_income_ttm_series

        dopont_df.loc[:, 'profit_margin'] = \
            income_statements_df['net_profit'] / income_statements_df['operations_income']
        dopont_df.loc[:, 'profit_margin_ttm'] = \
            net_profit_ttm_series / operations_income_ttm_series

        dopont_df.loc[:, 'asset_turnover_ttm'] = \
            operations_income_ttm_series / total_assets_mean

        dopont_df.loc[:, 'equity_multiplier_ttm'] = \
            total_assets_mean / total_shareholders_equity_mean

        dopont_df = dopont_df.dropna().sort_index()

        # Save all results into the database
        latest_dopont_index = dopont_df.tail(1)
        latest_index, _ = LatestIndex.objects.update_or_create(
            stock=stock,
            defaults={
                'gross_margin': latest_dopont_index['gross_margin'],
                'gross_margin_ttm': latest_dopont_index['gross_margin_ttm'],
                'profit_margin': latest_dopont_index['profit_margin'],
                'profit_margin_ttm': latest_dopont_index['profit_margin_ttm'],
                'asset_turnover_ttm': latest_dopont_index['asset_turnover_ttm'],
                'equity_multiplier_ttm': latest_dopont_index['equity_multiplier_ttm']
            })
        latest_index.save()

        for row in dopont_df.iterrows():
            historical_kpi, _ = HistoricalKpi.objects.update_or_create(
                stock=stock, report_date=row[0],
                defaults={
                    'gross_margin': row[1]['gross_margin'],
                    'gross_margin_ttm': row[1]['gross_margin_ttm'],
                    'profit_margin': row[1]['profit_margin'],
                    'profit_margin_ttm': row[1]['profit_margin_ttm'],
                    'asset_turnover_ttm': row[1]['asset_turnover_ttm'],
                    'equity_multiplier_ttm': row[1]['equity_multiplier_ttm']
                })
            historical_kpi.save()
