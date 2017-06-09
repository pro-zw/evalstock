# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^resourceful/china-stocks/([0-9]{6}\.(?:(?:sh)|(?:sz)))/$', views.china_stock),
]
