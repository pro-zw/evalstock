from django.contrib import admin

from .models import LatestIndex, HistoricalKpi


class LatestIndexAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 
        'get_industry', 'get_market_value',
        'roce', 'roce_ttm', 'earnings_yield', 'net_profit_reality')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field = 'stock__stock_code'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.admin_order_field = 'stock__stock_name'
    get_stock_name.short_description = 'Stock Name'

    def get_industry(self, obj):
        return obj.stock.industry
    get_industry.admin_order_field = 'stock__industry'
    get_industry.short_description = 'Industry'

    def get_market_value(self, obj):
        return obj.stock.market_value
    get_market_value.admin_order_field = 'stock__market_value'
    get_market_value.short_description = 'Market Value'


class HistoricalKpiAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date',
        'roce', 'roce_ttm', 'net_profit_reality')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field = 'stock__stock_code'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.admin_order_field = 'stock__stock_name'
    get_stock_name.short_description = 'Stock Name'

admin.site.register(LatestIndex, LatestIndexAdmin)
admin.site.register(HistoricalKpi, HistoricalKpiAdmin)
