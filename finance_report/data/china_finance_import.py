# -*- coding: utf-8 -*-
"""Import relevant chinese stock financial data into the database.

The financial data imported forms the basic of all different financial
analysis models, such as magic formula and DuPont analysis

"""


import pandas as pd
from django.db.models import Q

from finance_report.models import (
    Stock, ChinaBalanceSheet, ChinaCashFlowStatement, ChinaIncomeStatement)


def main(skip_existing_date: bool = False):
    """Import the relevant financial data
    
    :param skip_existing_date: skip existing date in the database
    
    """

    all_finance_data_df = (pd.read_csv(
        './finance_report/data/china_all_financial_data.csv',
        index_col=['股票代码'], parse_dates=True)
        .fillna(value=0.0, axis=1))

    # Load stock information from the database
    # Currently, our analysis does not handle the following industries
    for stock in Stock.objects.exclude(
            Q(industry__exact='电力行业') |
            Q(industry__exact='公路桥梁') |
            Q(industry__exact='交通运输') |
            Q(industry__exact='金融行业') |
            Q(industry__exact='供水供气') |
            Q(industry__isnull=True)):

        external_code = stock.external_code()
        stock_finance_data_df = (all_finance_data_df
                                 .loc[external_code]
                                 .sort_values(by='报告类型'))

        # TODO: Maybe provide a function to skip existing date in the database
        stock.financial_report_date = stock_finance_data_df['报告类型'].iloc[-1]
        stock.save()

        for row in stock_finance_data_df.iterrows():
            finance_data = row[1]

            # 资产负债表
            balance_sheet, created = ChinaBalanceSheet.objects.update_or_create(
                stock=stock, report_date=finance_data['报告类型'],
                defaults={
                    'current_assets': finance_data['流动资产合计'],
                    'cash': finance_data['货币资金'],
                    'trading_financial_assets': finance_data['交易性金融资产'],
                    'fixed_assets_net_value': finance_data['固定资产净额'],
                    'investment_real_estates': finance_data['投资性房地产净额'],
                    'current_liabilities': finance_data['流动负债合计'],
                    'short_term_borrowings': finance_data['短期借款'],
                    'notes_payable': finance_data['应付票据'],
                    'non_current_liabilities_due': finance_data['一年内到期的非流动负债'],
                    'long_term_borrowings': finance_data['长期借款'],
                    'debt_securities_issued': finance_data['应付债券'],
                    'goodwill': finance_data['商誉净额'],
                    'minority_shareholders_equity': finance_data['少数股东权益'],
                    'available_for_sale_financial_assets': finance_data['可供出售金融资产净额'],
                    'held_to_maturity_investments': finance_data['持有至到期投资净额'],
                    'deferred_tax_liabilities': finance_data['递延所得税负债'],
                    'equity_to_parent_company_shareholders': finance_data['归属于母公司所有者权益合计'],
                    'total_shareholders_equity': finance_data['所有者权益合计'],
                    'total_assets': finance_data['资产总计']
                })
            balance_sheet.save()

            # 利润表
            income_statement, created = ChinaIncomeStatement.objects.update_or_create(
                stock=stock, report_date=finance_data['报告类型'],
                defaults={
                    'operations_income': finance_data['营业收入'],
                    'income_from_joint': finance_data['其中：对联营企业和合营企业的投资收益'],
                    'operations_costs': finance_data['营业成本'],
                    'taxes_and_surcharges': finance_data['营业税金及附加'],
                    'admin_expenses': finance_data['管理费用'],
                    'selling_expenses': finance_data['销售费用'],
                    'financial_expenses': finance_data['财务费用'],
                    'net_profit_to_parent_company_shareholders': finance_data['归属于母公司所有者的净利润'],
                    'minority_interest_income': finance_data['少数股东损益'],
                    'net_profit': finance_data['净利润']
                })
            income_statement.save()

            # 现金流量表
            cash_flow_statement, created = ChinaCashFlowStatement.objects.update_or_create(
                stock=stock, report_date=finance_data['报告类型'],
                defaults={
                    'net_cash_flows_from_operating_activities': finance_data['经营活动产生的现金流量净额'],
                    'net_cash_flows_from_investing_activities': finance_data['投资活动产生的现金流量净额'],
                    'net_cash_flows_from_financing_activities': finance_data['筹资活动产生的现金流量净额']
                })
            cash_flow_statement.save()
