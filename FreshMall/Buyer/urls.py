from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path("index/",index),       # 首页
    path("login/",login),       # 登录页
    path("register/",register),  # 注册页
    path("logout/",logout),     # 退出登录
    path("goods_list/", goods_list),  # 商品列表页
    path("cart/", cart),         # 购物车页
    path("add_cart/", add_cart),         # 向购物车添加商品
    path("detail/",detail),     # 商品详情页
    path("order/",order),         # 提交订单页
    path("pay_order/",pay_order),   # 支付页
    path("pay_result/",pay_result), # 支付结果返回页面
]

urlpatterns += [
    path("base/", base),
]
