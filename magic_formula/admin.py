# -*- coding: utf-8 -*-

from django.contrib import admin

from finance_report.admin import StockAdminMixin
from .models import LatestIndex, HistoricalKpi


class LatestIndexAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 
        'get_industry', 'get_market_value',
        'roce', 'roce_ttm', 'earnings_yield', 'net_profit_reality')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_industry(self, obj):
        return obj.stock.industry
    get_industry.admin_order_field = 'stock__industry'
    get_industry.short_description = 'Industry'

    def get_market_value(self, obj):
        return obj.stock.market_value
    get_market_value.admin_order_field = 'stock__market_value'
    get_market_value.short_description = 'Market Value'


class HistoricalKpiAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date',
        'roce', 'roce_ttm', 'net_profit_reality')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']


admin.site.register(LatestIndex, LatestIndexAdmin)
admin.site.register(HistoricalKpi, HistoricalKpiAdmin)
