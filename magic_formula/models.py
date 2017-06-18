from django.db import models

import finance_report.models as finance_report_models


class LatestIndex(models.Model):
    # 股票
    stock = models.OneToOneField(
        finance_report_models.Stock,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='magic_formula_latest_index'
    )

    # 息税前利润（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint = models.FloatField('ebit without investment income from joint ventures and affiliates')
    # 息税前利润 TTM（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint_ttm = models.FloatField('ebit ttm without investment income from joint ventures and affiliates')
    # 息税前利润（包含对联营企业和合营企业的投资收益）
    ebit_with_joint = models.FloatField('ebit with investment income from joint ventures and affiliates')
    # 息税前利润 TTM（包含对联营企业和合营企业的投资收益）
    ebit_with_joint_ttm = models.FloatField('ebit ttm with investment income from joint ventures and affiliates')
    # 资本回报率 = EBIT/(净流动资产 + 净固定资产)
    roce = models.FloatField('return on capital employed')
    # 资本回报率 TTM = EBIT_TTM/(净流动资产 + 净固定资产)
    roce_ttm = models.FloatField('return on capital employed ttm')
    # 收益率 = EBIT/企业价格，这里使用的是 EBIT TTM 数据
    earnings_yield = models.FloatField('earnings yield')
    # 净利润真实性指标 = 经营活动产生的现金流量净额/净利润
    net_profit_reality = models.FloatField('net profit reality')


class HistoricalKpi(models.Model):
    # 股票
    stock = models.ForeignKey(
        finance_report_models.Stock,
        on_delete=models.CASCADE,
        related_name='magic_formula_historical_kpi'
    )

    # 报告日期
    report_date = models.DateField('report date')
    # 息税前利润（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint = models.FloatField('ebit without investment income from joint ventures and affiliates')
    # 息税前利润 TTM（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint_ttm = models.FloatField('ebit ttm without investment income from joint ventures and affiliates')
    # 息税前利润（包含对联营企业和合营企业的投资收益）
    ebit_with_joint = models.FloatField('ebit with investment income from joint ventures and affiliates')
    # 息税前利润 TTM（包含对联营企业和合营企业的投资收益）
    ebit_with_joint_ttm = models.FloatField('ebit ttm with investment income from joint ventures and affiliates')
    # 资本回报率
    roce = models.FloatField('return on capital employed')
    # 资本回报率 TTM = EBIT_TTM/(净流动资产 + 净固定资产)
    roce_ttm = models.FloatField('return on capital employed ttm')
    # 净利润真实性指标 = 经营活动产生的现金流量净额/净利润
    net_profit_reality = models.FloatField('net profit reality')

    class Meta:
        unique_together = (('stock', 'report_date'),)
