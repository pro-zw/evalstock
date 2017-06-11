# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resourceful/v1/stock/([0-9]{6}\.[a-z]+)/historical_kpi$', views.historical_kpi),
]
