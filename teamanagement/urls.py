#!/usr/bin/env python
# @Time    : 2018/12/22 19:27
# @Author  : wb
# @File    : urls.py

# 用于配置urls

from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('purchase_create', views.purchase_create),
    path('purchase_input', views.purchase_input),
    path('purchase_show', views.purchase_show),
    path('purchase_detail/<int:purchase_id>', views.purchase_detail, name='detail'),
    path('purchase_del', views.purchase_del),
    path('warehouse_confirm', views.warehouse_confirm),
    path('purchase_confirm', views.purchase_confirm),
    path('purchase_wrong', views.purchase_wrong),
    path('warehouse_goodscheck', views.warehouse_goodscheck),
    path('warehouse_goodsdetail/<int:goods_id>', views.warehouse_goodsdetail),
    path('sales_create', views.sales_create),
    path('tea_buy', views.tea_buy),
    path('sales_input', views.sales_input),
    path('sales_show', views.sales_show),
    path('sales_detail/<int:sales_id>', views.sales_detail),
    path('finance_show', views.finance_show),
    path('', views.login_show),
    path('login', views.login),
    path('logout', views.logout)
    #path('finance_detail', views.finance_detail),
]