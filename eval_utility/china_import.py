# -*- coding: utf-8 -*-

import numpy as np
from pandas import Series, DataFrame
import pandas as pd

# from finance_report.models import Stock, ChinaBalanceSheet, ChinaIncomeStatement, ChinaCashFlowStatement, CompanyHistoricalKpi
import finance_report.models as finance_report_models
import magic_formula.models as magic_formula_models

# 读取历史财务报告并删除与股票报价表格重复的列表项
all_financial_report_df = (pd.read_csv('./eval_utility/china_all_financial_data.csv', 
                                      index_col=['股票代码'], parse_dates=True).fillna(value=0.0, axis=1)
                                      .drop(['收盘价', 
                                             '流通市值',
                                             '总市值',
                                             '股票名称'], axis=1))

# 读取股票最新市场数据
stock_quote_df = pd.read_csv('./eval_utility/china_stock_overview.csv',
                             index_col=['股票代码'], parse_dates=True)

financial_report_date_chosen = '2016-12-31'

# 合并两份表格并移除金融与公用事业股票
financial_report_df = all_financial_report_df[all_financial_report_df['报告类型'] == financial_report_date_chosen]      
stock_df = pd.concat([financial_report_df, stock_quote_df], axis=1, join_axes=[financial_report_df.index])
stock_df = stock_df[-(stock_df['新浪行业'] == '电力行业')]
stock_df = stock_df[-(stock_df['新浪行业'] == '公路桥梁')]
stock_df = stock_df[-(stock_df['新浪行业'] == '交通运输')]
stock_df = stock_df[-(stock_df['新浪行业'] == '金融行业')]
stock_df = stock_df[-(stock_df['新浪行业'] == '供水供气')]

print(len(financial_report_df))
print(len(stock_df))

# 提取出感兴趣的列
stock_overview_df = (stock_df[['股票名称', 
                               '交易日期', 
                               '总市值', 
                               '新浪行业', 
                               '报告类型', 
                               '流动资产合计',
                               '货币资金',
                               '交易性金融资产',
                               '固定资产净额',
                               '投资性房地产净额',
                               '流动负债合计',
                               '短期借款',
                               '应付票据',
                               '一年内到期的非流动负债',
                               '营业收入',
                               '其中：对联营企业和合营企业的投资收益',
                               '营业成本',
                               '营业税金及附加', # 在 2016 的企业年报中该项重命名为税金及附加
                               '管理费用',
                               '销售费用',
                               '长期借款',
                               '应付债券',
                               '少数股东权益',
                               '可供出售金融资产净额',
                               '持有至到期投资净额',
                               '递延所得税负债',
                               '归属于母公司所有者权益合计',
                               '所有者权益合计',
                               '归属于母公司所有者的净利润',
                               '净利润',
                               '经营活动产生的现金流量净额',
                               '投资活动产生的现金流量净额',
                               '筹资活动产生的现金流量净额'
                               ]]
                    .dropna()
                    .reset_index()
                    .drop_duplicates(subset='股票代码', keep='last')
                    .set_index('股票代码')
                    )
print(len(stock_overview_df))

# Stock.objects.all().delete()
for (code,
     name,
     market_data_date,
     market_value,
     industry,
     financial_report_date,
     current_assets,
     cash,
     trading_financial_assets,
     fixed_assets_net_value,
     investment_real_estates,
     current_liabilities,
     short_term_borrowings,
     notes_payable,
     non_current_liabilities_due,
     operations_income,
     income_from_joint,
     operations_costs,
     taxes_and_surcharges,
     admin_expenses,
     selling_expenses,
     long_term_borrowings,
     debt_securities_issued,
     minority_shareholders_equity,
     available_for_sale_financial_assets,
     held_to_maturity_investments,
     deferred_tax_liabilities,
     equity_to_parent_company_shareholders,
     total_shareholders_equity,
     net_profit_to_parent_company_shareholders,
     net_profit,
     net_cash_flows_from_operating_activities,
     net_cash_flows_from_investing_activities,
     net_cash_flows_from_financing_activities
     ) in stock_overview_df.itertuples():
    
    # 超额现金
    excess_cash = max(0, 
                      (cash + trading_financial_assets) 
                       - max(0, current_liabilities - (current_assets - (cash + trading_financial_assets))))
    
    # 息税前利润（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint = (operations_income
                          - operations_costs 
                          - taxes_and_surcharges
                          - admin_expenses
                          - selling_expenses)
    
    # 息税前利润（包含对联营企业和合营企业的投资收益）
    ebit_with_joint = (operations_income
                       - operations_costs 
                       - taxes_and_surcharges
                       - admin_expenses
                       - selling_expenses
                       + income_from_joint)
    # 资本回报率 = EBIT/(净流动资产 + 净固定资产)
    roic = (ebit_without_joint
            / (current_assets 
               - current_liabilities
               - excess_cash
               + short_term_borrowings
               + notes_payable
               + non_current_liabilities_due
               + fixed_assets_net_value
               + investment_real_estates
               ))
    
    # 收益率 = EBIT/企业价格
    earnings_yield = (ebit_with_joint
                      / (market_value 
                         + short_term_borrowings
                         + notes_payable
                         + non_current_liabilities_due
                         + long_term_borrowings
                         + debt_securities_issued
                         + minority_shareholders_equity
                         - available_for_sale_financial_assets
                         - held_to_maturity_investments
                         + deferred_tax_liabilities
                         - excess_cash
                         ))
    
    code = code[2:] + '.' + code[0:2]
    
    # 股票概览表
    stock, created = finance_report_models.Stock.objects.update_or_create(
        stock_code=code,
        defaults = {
            'stock_name': name,
            'industry': industry,
            'financial_report_date': financial_report_date,
            'market_data_date': market_data_date,
            'market_value': market_value
        })
    stock.save()
    
    magic_formula_stock, created = magic_formula_models.Stock.objects.update_or_create(
        stock = stock,
        defaults = {
            'ebit_without_joint': ebit_without_joint,
            'ebit_with_joint': ebit_with_joint,
            'roic': roic,
            'earnings_yield': earnings_yield,
            'net_profit_reality': net_cash_flows_from_operating_activities / net_profit
        })
    magic_formula_stock.save()
    
    # 公司关键业绩指标历史记录表
    historical_kpi, created = magic_formula_models.HistoricalKpi.objects.update_or_create(
        stock = stock, report_date = financial_report_date,    
        defaults = {
            'ebit_without_joint': ebit_without_joint,
            'ebit_with_joint': ebit_with_joint,
            'roic': roic
        })
    historical_kpi.save()    
    
    # 资产负债表
    balance_sheet, created = finance_report_models.ChinaBalanceSheet.objects.update_or_create(
        stock = stock, report_date = financial_report_date,    
        defaults = {
            'current_assets': current_assets,
            'cash': cash,
            'trading_financial_assets': trading_financial_assets,
            'fixed_assets_net_value': fixed_assets_net_value,
            'investment_real_estates': investment_real_estates,
            'current_liabilities': current_liabilities,
            'short_term_borrowings': short_term_borrowings,
            'notes_payable': notes_payable,
            'non_current_liabilities_due': non_current_liabilities_due,
            'long_term_borrowings': long_term_borrowings,
            'debt_securities_issued': debt_securities_issued,
            'minority_shareholders_equity': minority_shareholders_equity,
            'available_for_sale_financial_assets': available_for_sale_financial_assets,
            'held_to_maturity_investments': held_to_maturity_investments,
            'deferred_tax_liabilities': deferred_tax_liabilities,
            'equity_to_parent_company_shareholders': equity_to_parent_company_shareholders,
            'total_shareholders_equity': total_shareholders_equity
        })
    balance_sheet.save()
    
    # 利润表
    income_statement, created = finance_report_models.ChinaIncomeStatement.objects.update_or_create(
        stock = stock, report_date = financial_report_date,    
        defaults = {
            'operations_income': operations_income,
            'operations_costs': operations_costs,
            'taxes_and_surcharges': taxes_and_surcharges,
            'admin_expenses': admin_expenses,
            'selling_expenses': selling_expenses,
            'net_profit_to_parent_company_shareholders': net_profit_to_parent_company_shareholders,
            'net_profit': net_profit
        })
    income_statement.save()
    
    # 现金流量表
    cash_flow_statement, created = finance_report_models.ChinaCashFlowStatement.objects.update_or_create(
        stock = stock, report_date = financial_report_date,    
        defaults = {
            'net_cash_flows_from_operating_activities': net_cash_flows_from_operating_activities,
            'net_cash_flows_from_investing_activities': net_cash_flows_from_investing_activities,
            'net_cash_flows_from_financing_activities': net_cash_flows_from_financing_activities
        })
    cash_flow_statement.save()
    