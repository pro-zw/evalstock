from django.contrib import admin

from finance_report.admin import StockAdminMixin
from .models import LatestIndex, HistoricalKpi


class LatestIndexAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name',
        'gross_margin', 'gross_margin_ttm',
        'profit_margin', 'profit_margin_ttm',
        'asset_turnover_ttm', 'equity_multiplier_ttm')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']


class HistoricalKpiAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name',
        'gross_margin', 'gross_margin_ttm',
        'profit_margin', 'profit_margin_ttm',
        'asset_turnover_ttm', 'equity_multiplier_ttm')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']


admin.site.register(LatestIndex, LatestIndexAdmin)
admin.site.register(HistoricalKpi, HistoricalKpiAdmin)