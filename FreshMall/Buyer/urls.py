from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path("index/",index),
    path("login/",login),
    path("register/",register),
    path("logout/",logout),
    path("goods_list/",goods_list),
    path("cart/",cart),
    path("detail/",detail),
    path("pay_order/",pay_order),
    path("pay_result/",pay_result),
]

urlpatterns += [
    path("base/",base)
]
