# -*- coding: utf-8 -*-

from django.db import models


class Stock(models.Model):
    stock_code = models.CharField(max_length=128, unique=True)
    stock_name = models.CharField(max_length=256)
    industry = models.CharField(max_length=128, default=None, blank=True, null=True)

    # 最新数据所依赖的财报与市场数据日期
    financial_report_date = models.DateField('financial report date', default=None, blank=True, null=True)
    market_data_date = models.DateField('market data date', default=None, blank=True, null=True)

    # 总市值
    market_value = models.FloatField('market value', default=None, blank=True, null=True)

    @classmethod
    def internal_code(cls, external_code: str, country: str) -> str:
        """Convert the stock code from external presentation to
        the internal presentation
        
        :param external_code: The external presentation of the stock code
        :param country: The country of the stock
        :return: The internal presentation of the stock code
        """

        if country == 'China':
            return external_code[2:] + '.' + external_code[0:2]
        elif country == 'Australia':
            return external_code + '.asx'

        raise Exception('Unsupported country of stocks')

    def external_code(self) -> str:
        """Convert the stock code from internal presentation to
        the external presentation
        
        :return: The external presentation of the stock code
        """

        code_components = self.stock_code.split('.')
        country_suffix = code_components[1]
        if country_suffix == 'sh' or country_suffix == 'sz':
            return country_suffix + code_components[0]
        elif country_suffix == 'asx':
            return code_components[0]

        raise Exception('Unsupported country of stocks')

    def __str__(self):
        return '%s (%s)' % (self.stock_code, self.stock_name)


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
    fixed_assets_net_value = models.FloatField('fixed assets net value')
    # 投资性房地产
    investment_real_estates = models.FloatField('investment real estates')
    # 流动负债
    current_liabilities = models.FloatField('current liabilities')
    # 短期借款
    short_term_borrowings = models.FloatField('short-term borrowings')
    # 应付票据
    notes_payable = models.FloatField('notes payable')
    # 一年内到期的非流动负债
    non_current_liabilities_due = models.FloatField('Non-current liabilities maturing within one year')
    # 应付短期借款
    # short_term_debt_securities = models.FloatField('Short-term debt securities issued')
    # 长期借款
    long_term_borrowings = models.FloatField('long-term borrowings')
    # 应付债券
    debt_securities_issued = models.FloatField('debt securities issued')
    # 商誉
    goodwill = models.FloatField('goodwill')
    # 少数股东权益
    minority_shareholders_equity = models.FloatField('minority shareholders equity')
    # 可供出售金融资产
    available_for_sale_financial_assets = models.FloatField('available-for-sale financial assets')
    # 持有到期投资
    held_to_maturity_investments = models.FloatField('held-to-maturity investments')
    # 递延所得税负债
    deferred_tax_liabilities = models.FloatField('deferred tax liabilities')
    # 归属于母公司所有者权益合计
    equity_to_parent_company_shareholders = models.FloatField(
        'total equity attributable to the shareholders of parent company')
    # 所有者权益合计
    total_shareholders_equity = models.FloatField('total shareholders equity')
    # 总资产
    total_assets = models.FloatField('total assets')

    class Meta:
        unique_together = (('stock', 'report_date'),)


class ChinaIncomeStatement(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 营业收入
    operations_income = models.FloatField('Income from operations')
    # 对联营企业和合营企业的投资收益
    income_from_joint = models.FloatField('Income from joint')
    # 营业成本
    operations_costs = models.FloatField('costs of operations')
    # 税金及附加
    taxes_and_surcharges = models.FloatField('taxes and surcharges')
    # 管理费用
    admin_expenses = models.FloatField('general and administrative expenses')
    # 销售费用
    selling_expenses = models.FloatField('selling and distribution expenses')
    # 财务费用
    financial_expenses = models.FloatField('financial expenses')
    # 归属于母公司所有者的净利润
    net_profit_to_parent_company_shareholders = models.FloatField(
        'net profit attributable to shareholders of parent company')
    # 少数股东损益
    minority_interest_income = models.FloatField('minority interest income')
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


class AustraliaBalanceSheet(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 流动资产
    current_assets = models.FloatField('current assets')
    # 货币资金
    cash = models.FloatField('Cash and cash equivalents')
    # 流动负债
    current_liabilities = models.FloatField('current liabilities')
    # 流动或有负债
    current_provisions = models.FloatField('current provisions')
    # 非流动负债
    non_current_liabilities = models.FloatField('non-current liabilities')
    # 非流动或有负债
    non_current_provisions = models.FloatField('non-current provisions')
    # 净资产
    net_assets = models.FloatField('net assets')
    # 总资产
    total_assets = models.FloatField('total assets')
    # 无形资产
    intangible_assets = models.FloatField('intangible assets')
    # 固定资产净值
    fixed_assets_net_value = models.FloatField('fixed assets net value')
    # 短期各项应付款与借款
    short_term_payables_and_borrowings = models.FloatField('short term payables and borrowings')
    # 长期各项应付款与借款
    long_term_payables_and_borrowings = models.FloatField('long term payables and borrowings')
    # 递延所得税负债
    deferred_tax_liabilities = models.FloatField('deferred tax liabilities')
    # TODO: 投资性房地产与交易性金融资产

    class Meta:
        unique_together = (('stock', 'report_date'),)


class AustraliaIncomeStatement(models.Model):
    # 股票
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 营业收入
    revenue = models.FloatField('revenue')
    # 息税前利润（常规经营活动）
    profit_before_interest_and_tax = models.FloatField('profit before interest and taxes')
    # 净利润
    profit = models.FloatField('profit for the period')
    # 综合收益
    total_comprehensive_income = models.FloatField('total comprehensive income')

    class Meta:
        unique_together = (('stock', 'report_date'),)


class AustraliaCashFlowStatement(models.Model):
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
