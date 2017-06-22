from django.db import models

import finance_report.models as finance_report_models


class LatestIndex(models.Model):
    # 股票
    stock = models.OneToOneField(
        finance_report_models.Stock,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='dopont_analysis_latest_index'
    )

    # 主营业务毛利率
    gross_margin = models.FloatField('gross margin')
    # 主营业务毛利率 TTM
    gross_margin_ttm = models.FloatField('gross margin ttm')
    # 销售毛利率
    profit_margin = models.FloatField('profit margin')
    # 销售毛利率 TTM
    profit_margin_ttm = models.FloatField('profit margin ttm')
    # 资产周转率 TTM
    asset_turnover_ttm = models.FloatField('asset turnover ttm')
    # 权益乘数 TTM
    equity_multiplier_ttm = models.FloatField('equity multiplier ttm')


class HistoricalKpi(models.Model):
    # 股票
    stock = models.ForeignKey(
        finance_report_models.Stock,
        on_delete=models.CASCADE,
        related_name='dopont_analysis_historical_kpi'
    )

    # 报告日期
    report_date = models.DateField('report date')
    # 主营业务毛利率
    gross_margin = models.FloatField('gross margin')
    # 主营业务毛利率 TTM
    gross_margin_ttm = models.FloatField('gross margin ttm')
    # 销售毛利率
    profit_margin = models.FloatField('profit margin')
    # 销售毛利率 TTM
    profit_margin_ttm = models.FloatField('profit margin ttm')
    # 资产周转率 TTM
    asset_turnover_ttm = models.FloatField('asset turnover ttm')
    # 权益乘数 TTM
    equity_multiplier_ttm = models.FloatField('equity multiplier ttm')
