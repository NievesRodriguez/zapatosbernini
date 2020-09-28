from django.urls import path, include, re_path
from . import views


urlpatterns = [
    re_path(r'^login$', views.login),
    path('',views.index),
    re_path(r'^verproductos$', views.verproductos),
               
]        