from django.contrib import admin

from .models import Stock, ChinaBalanceSheet, ChinaIncomeStatement, ChinaCashFlowStatement

class StockAdmin(admin.ModelAdmin):
    list_display = (
        'stock_code', 'stock_name', 'industry', 
        'financial_report_date', 'market_data_date', 'market_value')
    list_per_page = 30
    search_fields = ['stock_code', 'stock_name']

class ChinaBalanceSheetAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'current_assets', 'cash', 'trading_financial_assets',
        'fixed_assets_net_value', 'investment_real_estates',
        'short_term_borrowings', 'notes_payable', 'non_current_liabilities_due', 'current_liabilities',
        'long_term_borrowings', 'debt_securities_issued', 'available_for_sale_financial_assets', 
        'held_to_maturity_investments', 'deferred_tax_liabilities', 
        'equity_to_parent_company_shareholders', 'minority_shareholders_equity')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field  = 'stock'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.short_description = 'Stock Name'

    fieldsets = [
        (None,                   {'fields': ['stock', 'report_date']}),
        ('Current assets',       {'fields': ['current_assets']}),
        ('Non-current assets',   {'fields': ['fixed_assets_net_value', 'investment_real_estates']}),
        ('Current liabilities',  {'fields': ['short_term_borrowings', 'notes_payable',
                                             'non_current_liabilities_due', 'current_liabilities']}),
    ]

class ChinaIncomeStatementAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'operations_income', 'operations_costs', 'taxes_and_surcharges',
        'admin_expenses', 'selling_expenses',
        'net_profit_to_parent_company_shareholders', 'net_profit')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field  = 'stock'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.short_description = 'Stock Name'

class ChinaCashFlowStatementAdmin(admin.ModelAdmin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'net_cash_flows_from_operating_activities', 
        'net_cash_flows_from_investing_activities', 
        'net_cash_flows_from_financing_activities')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field  = 'stock'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.short_description = 'Stock Name'

admin.site.register(Stock, StockAdmin)
admin.site.register(ChinaBalanceSheet, ChinaBalanceSheetAdmin)
admin.site.register(ChinaIncomeStatement, ChinaIncomeStatementAdmin)
admin.site.register(ChinaCashFlowStatement, ChinaCashFlowStatementAdmin)