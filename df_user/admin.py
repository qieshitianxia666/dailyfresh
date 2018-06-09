# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *
class UserInfoAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'uname', 'upwd', 'uemail', 'ushou', 'uaddress', 'uyoubian','uphone']
admin.site.register(UserInfo,UserInfoAdmin)