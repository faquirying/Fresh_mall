from django.db import models


class Seller(models.Model):
    """
        卖家信息模型类
    """
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    nickname = models.CharField(max_length=32, verbose_name="昵称", null=True,blank=True)
    phone = models.CharField(max_length=32, verbose_name="电话", null=True,blank=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    picture = models.ImageField(upload_to="store/images", verbose_name="用户头像", null=True, blank=True)
    address = models.CharField(max_length=32, verbose_name="地址", null=True, blank=True)

    card_id = models.CharField(max_length=32, verbose_name="身份证", null=True, blank=True)


class StoreType(models.Model):
    """
        店铺类型模型类
        与店铺是多对多关系
    """
    store_type = models.CharField(max_length=32,verbose_name="类型名称")
    type_descripton = models.TextField(verbose_name="类型名称")


class Store(models.Model):
    """
        店铺模型类
        与店铺类型多对多
        与商品一对多
    """
    store_name = models.CharField(max_length=32, verbose_name="店铺名称")
    store_address = models.CharField(max_length=32,verbose_name="店铺地址")
    store_descripton = models.TextField(verbose_name="店铺描述")
    store_logo = models.ImageField(upload_to="store/images",verbose_name="店铺logo")
    store_phone = models.CharField(max_length=32,verbose_name="店铺电话")
    store_money = models.FloatField(verbose_name="店铺注册资金")

    user_id = models.IntegerField(verbose_name="店铺主人")
    type = models.ManyToManyField(to=StoreType,verbose_name="店铺类型")


class GoodsType(models.Model):
    """
        商品类型模型类
        与商品是一对多关系
    """
    name = models.CharField(max_length=32,verbose_name="商品类型名称")
    description = models.TextField(verbose_name="商品类型描述")
    picture = models.ImageField(upload_to="buyer/images")


class Goods(models.Model):
    """
        商品模型类
        与商品类型多对一关系
        与店铺多对一关系
        与商品图片一对多关系
    """
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_image = models.ImageField(upload_to="store/images", verbose_name="商品图片")
    goods_number = models.IntegerField(verbose_name="商品数量库存")
    goods_resume = models.TextField(verbose_name="商品简述", null=True,blank=True)
    goods_description = models.TextField(verbose_name="商品描述")
    goods_date = models.DateField(verbose_name="出厂日期")
    goods_safeDate = models.IntegerField(verbose_name="保质期")
    goods_status = models.IntegerField(verbose_name="商品状态",default=1)  # 0 下架 1 待售

    goods_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,verbose_name="商品类型")
    store_id = models.ForeignKey(to=Store,on_delete=models.CASCADE,verbose_name="商品店铺")


class GoodsImg(models.Model):
    """
        商品图片模型类
        与商品是多对一关系
    """
    img_address = models.ImageField(upload_to="store/images",verbose_name="图片地址")
    img_description = models.TextField(max_length=32, verbose_name="图片描述")

    goods_id = models.ForeignKey(to = Goods,on_delete = models.CASCADE, verbose_name="商品id")

# Create your models here.
