# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Q

from .models import (Stock,
                     ChinaBalanceSheet, ChinaIncomeStatement, ChinaCashFlowStatement,
                     AustraliaBalanceSheet, AustraliaIncomeStatement, AustraliaCashFlowStatement)


class StockAdminMixin:
    # TODO: We need to filter stocks list when adding a financial report (separate Australia and Chinese stocks)

    def get_stock_code(self, obj):
        return obj.stock.stock_code
    get_stock_code.admin_order_field = 'stock'
    get_stock_code.short_description = 'Stock Code'

    def get_stock_name(self, obj):
        return obj.stock.stock_name
    get_stock_name.short_description = 'Stock Name'


class StockAdmin(admin.ModelAdmin):
    list_display = (
        'stock_code', 'stock_name', 'industry', 
        'financial_report_date', 'market_data_date', 'market_value')
    list_per_page = 30
    search_fields = ['stock_code', 'stock_name']


class ChinaBalanceSheetAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'current_assets', 'cash', 'trading_financial_assets',
        'fixed_assets_net_value', 'investment_real_estates',
        'short_term_borrowings', 'notes_payable', 'non_current_liabilities_due', 'current_liabilities',
        'long_term_borrowings', 'debt_securities_issued', 'available_for_sale_financial_assets', 
        'held_to_maturity_investments', 'goodwill', 'deferred_tax_liabilities',
        'equity_to_parent_company_shareholders', 'minority_shareholders_equity', 'total_shareholders_equity',
        'total_assets')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    fieldsets = [
        (None,                   {'fields': ['stock', 'report_date']}),
        ('Current assets',       {'fields': ['current_assets', 'cash', 'trading_financial_assets']}),
        ('Non-current assets',   {'fields': ['fixed_assets_net_value', 'investment_real_estates',
                                             'available_for_sale_financial_assets',
                                             'held_to_maturity_investments', 'goodwill']}),
        ('Total assets', {'fields': ['total_assets']}),
        ('Current liabilities',  {'fields': ['short_term_borrowings', 'notes_payable',
                                             'non_current_liabilities_due', 'current_liabilities']}),
        ('Non-current liabilities', {'fields': ['long_term_borrowings', 'debt_securities_issued',
                                                'non_current_liabilities_due', 'current_liabilities',
                                                'deferred_tax_liabilities']}),
        ('Owner equity', {'fields': ['equity_to_parent_company_shareholders',
                                     'minority_shareholders_equity',
                                     'total_shareholders_equity']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChinaBalanceSheetAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(
            Q(stock_code__endswith='.sh') | Q(stock_code__endswith='.sz')).order_by('stock_code')
        return form


class ChinaIncomeStatementAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'operations_income', 'operations_costs', 'taxes_and_surcharges',
        'admin_expenses', 'selling_expenses', 'financial_expenses',
        'net_profit_to_parent_company_shareholders', 'minority_interest_income', 'net_profit')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChinaIncomeStatementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(
            Q(stock_code__endswith='.sh') | Q(stock_code__endswith='.sz')).order_by('stock_code')
        return form


class ChinaCashFlowStatementAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date', 
        'net_cash_flows_from_operating_activities', 
        'net_cash_flows_from_investing_activities', 
        'net_cash_flows_from_financing_activities')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(ChinaCashFlowStatementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(
            Q(stock_code__endswith='.sh') | Q(stock_code__endswith='.sz')).order_by('stock_code')
        return form


class AustraliaBalanceSheetAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date',
        'current_assets', 'cash',
        'fixed_assets_net_value', 'intangible_assets',
        'current_liabilities', 'short_term_payables_and_borrowings', 'current_provisions',
        'non_current_liabilities', 'non_current_provisions',
        'net_assets',
        'total_assets')

    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    fieldsets = [
        (None,                   {'fields': ['stock', 'report_date']}),
        ('Current assets',       {'fields': ['cash', 'current_assets']}),
        ('Non-current assets',   {'fields': ['fixed_assets_net_value', 'intangible_assets']}),
        ('Total assets', {'fields': ['total_assets']}),
        ('Current liabilities',  {'fields': ['short_term_payables_and_borrowings',
                                             'current_provisions',
                                             'current_liabilities']}),
        ('Non-current liabilities', {'fields': ['long_term_payables_and_borrowings',
                                                'non_current_provisions',
                                                'deferred_tax_liabilities',
                                                'non_current_liabilities']}),
        ('Net assets', {'fields': ['net_assets']}),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(AustraliaBalanceSheetAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(stock_code__endswith='.asx').order_by('stock_code')
        return form


class AustraliaIncomeStatementAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date',
        'revenue', 'profit_before_interest_and_tax', 'total_comprehensive_income')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(AustraliaIncomeStatementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(stock_code__endswith='.asx').order_by('stock_code')
        return form


class AustraliaCashFlowStatementAdmin(admin.ModelAdmin, StockAdminMixin):
    list_display = (
        'get_stock_code', 'get_stock_name', 'report_date',
        'net_cash_flows_from_operating_activities',
        'net_cash_flows_from_investing_activities',
        'net_cash_flows_from_financing_activities')
    list_per_page = 30
    search_fields = ['stock__stock_code', 'stock__stock_name']

    def get_form(self, request, obj=None, **kwargs):
        form = super(AustraliaCashFlowStatementAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['stock'].queryset = Stock.objects.filter(stock_code__endswith='.asx').order_by('stock_code')
        return form

admin.site.register(Stock, StockAdmin)

admin.site.register(ChinaBalanceSheet, ChinaBalanceSheetAdmin)
admin.site.register(ChinaIncomeStatement, ChinaIncomeStatementAdmin)
admin.site.register(ChinaCashFlowStatement, ChinaCashFlowStatementAdmin)

admin.site.register(AustraliaBalanceSheet, AustraliaBalanceSheetAdmin)
admin.site.register(AustraliaIncomeStatement, AustraliaIncomeStatementAdmin)
admin.site.register(AustraliaCashFlowStatement, AustraliaCashFlowStatementAdmin)
