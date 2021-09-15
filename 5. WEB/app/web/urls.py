# -*- encoding: utf-8 -*-

from django.urls import path
from django.urls import re_path
from app.web import views

urlpatterns = [
    path("", views.index, name="home"),
    path("get_map_data/", views.get_map_data, name="get_map_data"),
    path("get_profile_data/", views.get_profile_data, name="get_profile_data"),
    path("load_cadastre_info/", views.load_cadastre_info, name="load_cadastre_info"),
    path("create_load/", views.create_load, name="create_load"),
    path("get_wallet_data/", views.get_wallet_data, name="get_wallet_data"),
    path("predict_load/", views.predict_load, name="predict_load"),
    path("estimate_property/", views.estimate_property, name="estimate_property"),
    re_path(r"^.*\.*", views.pages, name="pages"),
]
