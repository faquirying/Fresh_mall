from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('index/', index),
    path('out_login/', out_login),
    path('base/', base),
    path('register_store/', register_store),
    path('add_goods/', add_goods),
    path('add_goods_type/', add_goods_type),
    path('goods_type/', goods_type),
    re_path(r'list_goods/(?P<state>\w+)', list_goods),
    path('delete_goods_type/', delete_goods_type),
    # path('destroy/', destroy),
    re_path(r'set_goods/(?P<state>\w+)', set_goods),
    re_path(r'^descript_goods/(?P<goods_id>\d+)', descript_goods),
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods),
]

urlpatterns += [
    path('base/', base)
]
