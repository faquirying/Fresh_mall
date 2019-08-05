from django.urls import path,re_path
from Store.views import *
urlpatterns = [
    path('register/', register),      # 注册
    path('login/', login),            # 登录
    path('index/', index),            # 首页
    path('out_login/', out_login),    # 退出登录
    path('base/', base),              # base页
    path('register_store/', register_store),    # 店铺注册
    path('add_goods/', add_goods),              # 添加商品
    path('add_goods_type/', add_goods_type),    # 添加商品类型
    path('goods_type/', goods_type),            # 商品类型分页展示
    path('order_list/', order_list),            # 订单列表
    path('delete_order/', delete_order),            # 删除订单 new
    re_path(r'list_goods/(?P<state>\w+)', list_goods),  # 商品列表页
    path('delete_goods_type/', delete_goods_type),  # 删除商品类型
    re_path(r'set_goods/(?P<state>\w+)', set_goods),  # 商品上架下架
    re_path(r'^descript_goods/(?P<goods_id>\d+)', descript_goods),  # 商品描述
    re_path(r'update_goods/(?P<goods_id>\d+)', update_goods),  # 详情修改页
]

from django.views.decorators.cache import cache_page
urlpatterns += [
    path('base/', base),
    path('get_add/', get_add),
    path('swv/', cache_page(60*15)(small_white_view)),
    path('agl/', ajax_goods_list),  # ajax接口实现后台商品列表展示
    path('ajax_register/', ajax_register),  # 用户注册验证
]
