from django.contrib import admin

import finance_report.models as finance_report_models
from .models import Stock


class StockAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 
        'get_industry', 'get_market_value',
        'roce', 'earnings_yield', 'net_profit_reality', 'ebit_without_joint', 'ebit_with_joint')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field  = 'stock__stock_code'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.admin_order_field  = 'stock__stock_name'
    get_stock_name.short_description = 'Stock Name'

    def get_industry(self, obj):
        return obj.stock.industry
    get_industry.admin_order_field  = 'stock__industry'
    get_industry.short_description = 'Industry'

    def get_market_value(self, obj):
        return obj.stock.market_value
    get_market_value.admin_order_field  = 'stock__market_value'
    get_market_value.short_description = 'Market Value'


admin.site.register(Stock, StockAdmin)