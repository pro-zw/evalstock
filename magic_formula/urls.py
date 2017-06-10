# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resourceful/stock/([0-9]{6}\.[a-z]+)/historical_kpi$', views.historical_kpi),
]
