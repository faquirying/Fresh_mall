from django.db import models


# Create your models here.
class Buyer(models.Model):
    """
    买家模型类
        与收货地址是一对多关系
        包括用户名、密码、email、联系电话、联系地址
    """
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    email = models.EmailField(verbose_name="用户邮箱")
    phone = models.CharField(max_length=32,verbose_name="联系电话",null=True,blank=True)
    connect_address = models.TextField(verbose_name="联系地址",null=True,blank=True)


class Address(models.Model):
    """
    收货地址模型类
        与买家是多对一关系
        包括地址、收货人、收货人电话、邮编、买家id(外键关联)
    """
    address = models.TextField(verbose_name="收货地址")
    recver = models.CharField(max_length=32,verbose_name="收货人")
    recv_phone = models.CharField(max_length=32,verbose_name="收货人电话")
    post_number = models.CharField(max_length=32,verbose_name="邮编")
    buyer_id = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name="用户id")


class Order(models.Model):
    """
    订单模型类
        与买家是多对一关系
        与收货地址多对一关系
        包括订单id、商品数量、买家id(外键关联)、订单收货地址(外键关联)、订单总价、订单状态
        未支付------1 待发货--------2 已发货------3 已收货-----4 已退货------0
    """
    order_id = models.CharField(max_length=32,verbose_name="订单编号",blank=True,null=True)
    goods_count = models.IntegerField(verbose_name="商品数量")
    order_user = models.ForeignKey(to=Buyer,on_delete=models.CASCADE,verbose_name="订单用户")
    order_address = models.ForeignKey(to=Address,on_delete=models.CASCADE,verbose_name="订单地址",blank=True,null=True)
    order_price = models.FloatField(verbose_name="订单总价")
    order_status = models.IntegerField(verbose_name="订单状态")


class OrderDetail(models.Model):
    """
    订单详情模型类
        与订单多对一关系
        包括商品id、商品名称、商品价格、商品图片、购买数量、购买总价、商品所属店铺？
    """
    order_id = models.ForeignKey(to=Order,on_delete=models.CASCADE,verbose_name="订单编号(多对一)")
    goods_id = models.IntegerField(verbose_name="商品id")
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品单价")
    goods_image = models.ImageField(verbose_name="商品图片")
    goods_number = models.IntegerField(verbose_name="商品购买数量")
    goods_total = models.FloatField(verbose_name="购买商品的总价")
    goods_store = models.IntegerField(verbose_name="商品所属的商店id")


class Cart(models.Model):
    """
        购物车模型类
        先加入购物车，后生成订单
    """
    goods_name = models.CharField(max_length=32, verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_total = models.FloatField(verbose_name="商品总价")
    goods_number = models.IntegerField(verbose_name="商品数量")
    goods_picture = models.ImageField(upload_to="buyer/images", verbose_name="商品图片")
    goods_id = models.IntegerField(verbose_name="商品id")
    goods_store = models.IntegerField(verbose_name="商品商店")
    user_id = models.IntegerField(verbose_name="用户id")

