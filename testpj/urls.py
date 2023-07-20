"""testpj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views

urlpatterns = [
    path("show_res/", views.show_res),
    path("admin/", admin.site.urls),
    path("index/", views.index),
    path("show_comment_page/",views.show_comment_page),
    path("myorder/",views.myorder),

    #登录页面
    path("register/", views.register),
    path("login/", views.login),
    path("/", views.login),

    path("changepwd/", views.changepwd),
    #登录数据提交
    path("login_data/", views.login_data),
    path("register_data/", views.register_data),
    path("change_data/", views.change_data),

    #表格的增删查改
    path("showtable/",views.showtable),
    path("modify/",views.modify,name="modify"),
    path("modify_data/",views.modify_data,name="modify_data"),
    path("delete/",views.delete,name="delete"),
    path("insert/",views.insert,name="insert"),
    path("insert_data/",views.insert_data,name="insert_data"),

    path("show_comment/",views.show_comment,name="show_comment"),
    path("buy/",views.buy,name="buy"),
    path("check_all/",views.check_all,name="check_all"),
    path("tomindex/",views.tomindex,name="tomindex"),
    path("comment/",views.comment,name="commment"),
    path("delete_comment/",views.delete_comment,name="delete_comment"),
    path("show_order/",views.show_order,name="show_order"),
    path("show_order2/",views.show_order2,name="show_order2"),
    path("delete_order/",views.delete_order,name="delete_order"),
    path("update_order/",views.update_order,name="update_order"),

    path("pinfo/",views.pinfo,name="pinfo"),
    path("manage/",views.manage,name="manage"),











]
