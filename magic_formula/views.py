# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import json

from .models import HistoricalKpi
from misc_helper.json import date_serializer


@require_http_methods('GET')
def historical_kpi(request, stock_code: str):
    kpi_queryset = (HistoricalKpi.objects
                                 .filter(stock__stock_code=stock_code)
                                 .values('stock__stock_name',
                                         'report_date',
                                         'ebit_with_joint_ttm',
                                         'ebit_without_joint',
                                         'ebit_without_joint_ttm',
                                         'roce',
                                         'roce_ttm',
                                         'net_profit_reality')
                    )
    return HttpResponse(json.dumps(list(kpi_queryset),
                                   default=date_serializer), 'application/json')
