#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/19 15:35
# @Author  : Aries
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
import views


urlpatterns=[
    url(r'^$', views.cart),
    url(r'^add(\d+)_(\d+)/$', views.add),
    url(r'^edit(\d+)_(\d+)/$', views.edit),
    url(r'^delete(\d+)/$', views.delete),
]