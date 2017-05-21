# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone


class Stock(models.Model):
    stock_code = models.CharField(max_length=128, unique=True)
    stock_name = models.CharField(max_length=256)
    industry = models.CharField(max_length=128, default=None, blank=True, null=True)

    # 最新数据所依赖的财报与市场数据日期
    financial_report_date = models.DateField('financial report date', default=None, blank=True, null=True)
    market_data_date = models.DateField('market data date', default=None, blank=True, null=True)

    # 总市值
    market_value = models.FloatField('market value', default=None, blank=True, null=True)


class ChinaBalanceSheet(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 流动资产
    current_assets = models.FloatField('current assets')
    # 货币资金
    cash = models.FloatField('Cash and cash equivalents')
    # 交易性金融资产
    trading_financial_assets = models.FloatField('Financial assets held for trading')
    # 固定资产净值
    fixed_assets_net_value = models.FloatField('fixed assets-net value')
    # 投资性房地产
    investment_real_estates = models.FloatField('investment real estates', default=0)
    # 流动负债
    current_liabilities = models.FloatField('current liabilities')
    # 短期借款
    short_term_borrowings = models.FloatField('short-term borrowings', default=0)
    # 应付票据
    notes_payable = models.FloatField('notes payable', default=0)
    # 一年内到期的非流动负债
    non_current_liabilities_due = models.FloatField('Non-current liabilities maturing within one year', default=0)
    # 应付短期借款
    # short_term_debt_securities = models.FloatField('Short-term debt securities issued', default=0)
    # 长期借款
    long_term_borrowings = models.FloatField('long-term borrowings', default=0)
    # 应付债券
    debt_securities_issued = models.FloatField('debt securities issued', default=0)
    # 少数股东权益
    minority_shareholders_equity = models.FloatField('minority shareholders equity', default=0)
    # 可供出售金融资产
    available_for_sale_financial_assets = models.FloatField('available-for-sale financial assets', default=0)
    # 持有到期投资
    held_to_maturity_investments = models.FloatField('held-to-maturity investments', default=0)
    # 递延所得税负债
    deferred_tax_liabilities = models.FloatField('deferred tax liabilities', default=0)
    # 归属于母公司所有者权益合计
    equity_to_parent_company_shareholders = models.FloatField(
        'total equity attributable to the shareholders of parent company')
    # 所有者权益合计
    total_shareholders_equity = models.FloatField('total shareholders equity')

    class Meta:
        unique_together = (('stock', 'report_date'),)


class ChinaIncomeStatement(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 营业收入
    operations_income = models.FloatField('Income from operations')
    # 营业成本
    operations_costs = models.FloatField('costs of operations')
    # 税金及附加
    taxes_and_surcharges = models.FloatField('taxes and surcharges')
    # 管理费用
    admin_expenses = models.FloatField('general and administrative expenses')
    # 销售费用
    selling_expenses = models.FloatField('selling and distribution expenses')
    # 归属于母公司所有者的净利润
    net_profit_to_parent_company_shareholders = models.FloatField(
        'net profit attributable to shareholders of parent company')
    # 净利润
    net_profit = models.FloatField('net profit')

    class Meta:
        unique_together = (('stock', 'report_date'),)


class ChinaCashFlowStatement(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 经营活动产生的现金流量净额
    net_cash_flows_from_operating_activities = models.FloatField('net cash flows from operating activities')
    # 投资活动产生的现金流量净额
    net_cash_flows_from_investing_activities = models.FloatField('net cash flows from investing activities')
    # 筹资活动产生的现金流量净额 
    net_cash_flows_from_financing_activities = models.FloatField('net cash flows from financing activities')

    class Meta:
        unique_together = (('stock', 'report_date'),)


class AustraliaIncomeStatement(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 息税前利润（报表中可能被称为：profit from operations 或 profit before interest and income tax expense 等）
    earnings_before_interest_and_tax = models.IntegerField('earnings before interest and taxes')
