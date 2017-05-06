from django.db import models

import finance_report.models as finance_report_models

class Stock(models.Model):
    # 股票
    stock = models.ForeignKey(finance_report_models.Stock, on_delete=models.CASCADE)

    # 息税前利润（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint= models.FloatField('ebit without investment income from joint ventures and affiliates', default=0)
    # 息税前利润（包含对联营企业和合营企业的投资收益）
    ebit_with_joint= models.FloatField('ebit with investment income from joint ventures and affiliates', default=0)
	# 资本回报率 = EBIT/(净流动资产 + 净固定资产)
    roic = models.FloatField('return on invested capital', default=0)
    # 收益率 = EBIT/企业价格
    earnings_yield = models.FloatField('earnings yield', default=0)
    # 净利润真实性指标 = 经营活动产生的现金流量净额/净利润
    net_profit_reality = models.FloatField('net profit reality', default=0)

class HistoricalKpi(models.Model):
    # 股票
    stock = models.ForeignKey(finance_report_models.Stock, on_delete=models.CASCADE)

    # 报告日期
    report_date = models.DateField('report date')
    # 息税前利润（不包含对联营企业和合营企业的投资收益）
    ebit_without_joint= models.FloatField('ebit without investment income from joint ventures and affiliates')
    # 息税前利润（包含对联营企业和合营企业的投资收益）
    ebit_with_joint= models.FloatField('ebit with investment income from joint ventures and affiliates')
	# 资本回报率
    roic = models.FloatField('return on invested capital')

    class Meta:
        unique_together= (('stock', 'report_date'),)