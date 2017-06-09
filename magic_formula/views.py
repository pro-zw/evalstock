# -*- coding: utf-8 -*-

from django.shortcuts import render

from django.http import HttpResponse
import datetime


# TODO: Complete the API to return magic-formula kpi
def china_stock(request, stock_code: str):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s. The stock code is %s.</body></html>" % (now, stock_code)
    return HttpResponse(html)
