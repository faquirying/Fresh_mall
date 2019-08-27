import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from Store.models import *
from Buyer.models import *
# Create your views here.


# 密码加密
def set_password(password):
    # 实例化md5
    md5 = hashlib.md5()
    # 密码传值
    md5.update(password.encode())
    # md5.hexdigest()
    result = md5.hexdigest()
    return result


def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        # 获取前端提交的用户信息
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 如果不为空
        if username and password:
            # 检测Seller表中是否有该用户
            user = Seller.objects.filter(username=username).first()
            # 如果该用户名未被注册
            if not user:
                # 将用户信息存入Seller表当中
                seller = Seller()
                seller.username = username
                seller.password = set_password(password)
                seller.nickname = username
                seller.save()
                # 重定向到的登录页面
                return HttpResponseRedirect("/store/login/")
    # 否则留在注册页面
    return render(request, "store/register.html", locals())


# cookie 与 session 校验
def loginValid(fun):
    def inner(request, *args, **kwargs):
        # 获取cookie与session
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        # 如果cookie与session存在并且相同
        if c_user and s_user and c_user == s_user:
            # 返回要跳转的页面
            return fun(request, *args, **kwargs)
        else:
            # 否则重定向到登录页面
            return HttpResponseRedirect("/store/login")
    return inner


@loginValid
def index(request):
    """
    添加检查账号是否有店铺的逻辑
    """
    return render(request,"store/index.html")


def login(request):
    """
       登陆功能，如果登陆成功，跳转到index
       如果失败，跳转到login页
    """
    # 设置错误字典
    result = {"content": ""}
    # 如果登录校验不通过，返回登录界面
    response = render(request, "store/login.html", locals())
    # 设置cookie
    response.set_cookie("login_from", "login_page")
    if request.method == "POST":
        # 获取前端post过来的username和password
        username = request.POST.get("username")
        password = request.POST.get("password")
        # 如果username和password不为空
        if username and password:
            # 校验的是用户名是否存在
            user = Seller.objects.filter(username = username).first()
            if user:
                web_password = set_password(password)
                # 校验请求是否来源于登录界面
                cookies = request.COOKIES.get("login_from")
                # 校验密码是否正确
                if user.password == web_password and cookies == "login_page":  # 请求是否来源登录页面
                    response = HttpResponseRedirect("/store/index")
                    response.set_cookie("username", username)
                    response.set_cookie("user_id", user.id)  # cookie提供用户id方便其他功能查询
                    request.session["username"] = username
                    # 校验是否有店铺
                    store = Store.objects.filter(user_id=user.id).first()  # 再查询店铺是否存在
                    if store:
                        # 店铺存在，设置cookie “has_store” 为 店铺id
                        response.set_cookie("has_store", store.id)
                    else:
                        # 店铺不存子， 设置cookie “has_store” 为空
                        response.set_cookie("has_store", "")
                else:
                    result["content"] = "输入的密码有误，请重新输入"
            else:
                result["content"] = "用户名不存在"
        else:
            result["content"] = "用户名或密码不能为空"
    return response


# ajax注册校验
def ajax_register(request):
    result = {"status": "error", "content": ""}  # 初始化一个要返回的结果字典
    if request.method == "GET":
        username = request.GET.get("username")  # 获取ajax get请求过来的username
        # 获取到的 username 不为空
        if username:
            # 在seller表当中查找对应username
            user = Seller.objects.filter(username=username).first()
            if user:
                # user 不为空，用户名存在
                result["content"] = "用户名已存在"
            else:
                # user 为空，说明用户名可用
                result["status"] = "success"
                result["content"] = "用户名可以使用"
        else:
            result["content"] = "用户名不可以为空"
        print(result)
    return JsonResponse(result)


def out_login(request):
    # 退出登录后，回到登录页面
    response = HttpResponseRedirect('/store/login/')
    # 删除cookie
    response.delete_cookie('username')
    return response


def base(request):
    # base页视图
    return render(request,"store/base.html",locals())


# 添加店铺
@loginValid
def register_store(request):
    # 从店铺类型表当中获取所有的店铺类型
    type_list = StoreType.objects.all()
    if request.method == "POST":
        # 获取post来的各项内容
        post_data = request.POST  # 接收post数据
        store_name = post_data.get("store_name")
        store_descripton = post_data.get("store_descripton")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")

        # 通过cookie来得到user_id
        user_id = int(request.COOKIES.get("user_id"))
        # 通过request.post得到类型，但是是一个列表
        type_list = post_data.get("type")

        store_logo = request.FILES.get("store_logo")  # 通过request.FILES得到

        # 保存非多对多数据
        store = Store()
        store.store_name = store_name
        store.store_descripton = store_descripton
        store.store_phone = store_phone
        store.store_money = store_money
        store.store_address = store_address
        store.user_id = user_id
        store.store_logo = store_logo  # django1.8之后图片可以直接保存
        store.save()  # 保存，生成了数据库当中的一条数据
        # 在生成的数据当中添加多对多字段。
        for i in type_list:  # 循环type列表，得到类型id
            store_type = StoreType.objects.get(id=i)  # 查询类型数据
            store.type.add(store_type)  # 添加到类型字段，多对多的映射表
        store.save()  # 保存数据
        response = HttpResponseRedirect("/store/index")
        # 给用户添加 has_store
        response.set_cookie("has_store", store.id)
        return response
    return render(request, "store/register_store.html", locals())


def add_goods(request):
    """
        负责添加商品
    """
    goods_type_list = GoodsType.objects.all()
    if request.method == "POST":
        # 1. 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_resume = request.POST.get("goods_resume")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_store = request.POST.get("goods_store")
        goods_type = request.POST.get("goods_type")
        goods_image = request.FILES.get("goods_image")
        # 2. 开始保存数据
        goods = Goods()
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_resume = goods_resume
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.store_id = Store.objects.get(id=int(goods_store))
        goods.save()

        return HttpResponseRedirect("/store/list_goods/up/")
    return render(request, "store/add_goods.html", locals())


@loginValid
def list_goods(request,state):
    """
    商品的列表页
    """
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    # 获取两个关键字
    keywords = request.GET.get("keywords", "")  # 查询关键词
    page_num = request.GET.get("page_num", 1)  # 页码
    store_id = request.COOKIES.get("has_store")
    store = Store.objects.get(id=int(store_id))
    if keywords:  # 判断关键词是否存在
        goods_list = store.goods_set.filter(goods_name__contains=keywords, goods_status=state_num).order_by('-id')
        #  完成了模糊查询
    else:  # 如果关键词不存在，查询所有
        goods_list = store.goods_set.filter(goods_status=state_num).order_by('-id')
    # 分页，每页5条
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    print(page_range)
    # 返回分页数据
    return render(request, "store/list_goods.html", {"page": page, "page_range": page_range, "keywords": keywords, "state": state})


# 货物列表销毁项
def destroy(request):
    goods_id = request.GET.get("goods_id")
    # print(goods_id)
    del_id = Goods.objects.get(id=goods_id)
    del_id.delete()
    return HttpResponseRedirect("/store/list_goods/")


# 货物下架
def set_goods(request,state):
    if state == "up":
        state_num = 1
    else:
        state_num = 0
    id = request.GET.get("id")  # gei到id
    referer = request.META.get("HTTP_REFERER")  # 返回当前请求的来源地址
    if id:
        goods = Goods.objects.filter(id=int(id)).first()
        if state == "delete":
            goods.delete()
        else:
            goods.goods_status = state_num
            goods.save()
    return HttpResponseRedirect(referer)


# 列表详情页
@loginValid
def descript_goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    return render(request, "store/descript_goods.html", locals())


# 详情修改页
@loginValid
def update_goods(request,goods_id):
    goods_data = Goods.objects.filter(id=goods_id).first()
    if request.method == "POST":
        # 获取post请求
        goods_name = request.POST.get("goods_name")
        goods_price = request.POST.get("goods_price")
        goods_number = request.POST.get("goods_number")
        goods_description = request.POST.get("goods_description")
        goods_date = request.POST.get("goods_date")
        goods_safeDate = request.POST.get("goods_safeDate")
        goods_image = request.FILES.get("goods_image")
        # 修改数据
        goods = Goods.objects.get(id=int(goods_id))  # 获取当前商品
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_number = goods_number
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        # 如果有上传图片再发起修改
        if goods_image:
            goods.goods_image = goods_image
        goods.save()
        return HttpResponseRedirect("/store/descript_goods/%s/"%goods_id)
        # 保存多对多数据
    return render(request,"store/update_goods.html",locals())


def add_goods_type(request):
    if request.method == "POST":
        name = request.POST.get("name")
        print(name)
        picture = request.POST.get("picture")
        description = request.POST.get("description")
        goodtype = GoodsType()
        goodtype.name = name
        goodtype.picture = picture
        goodtype.description = description
        goodtype.save()
        return HttpResponseRedirect("/store/goods_type/")
    return render(request, "store/type_list_goods.html")


def goods_type(request):
    page_num = request.GET.get("page_num",1)  # 页码
    goods_type = GoodsType.objects.all()
    paginator = Paginator(goods_type, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    return render(request, "store/type_list_goods.html",locals())


def delete_goods_type(request):
    """
    删除商品类型
    """
    referer = request.META.get("HTTP_REFERER")
    id = request.GET.get("id")
    goods = GoodsType.objects.filter(id=int(id))
    goods.delete()
    return HttpResponseRedirect(referer)


def order_list(request):
    """
    订单列表
    """
    store_id = request.COOKIES.get("has_store")
    page_num = request.GET.get("page_num", 1)
    order_list = OrderDetail.objects.filter(order_id__order_status=2, goods_store=store_id)
    paginator = Paginator(order_list, 3)  # 展示的内容和每一页展示的数据的条数
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    # order = OrderDetail.objects.filter(goods_store=store_id)
    # order_list = order.order_set
    return render(request, "store/order_list.html", locals())


from rest_framework import viewsets

from Store.serializers import *
from django_filters.rest_framework import DjangoFilterBackend   # 导入过滤器


class UserViewSet(viewsets.ModelViewSet):
    """
    定义视图行为
    """
    queryset = Goods.objects.all()  # 具体返回的数据
    serializer_class = UserSerializer  # 指定过滤的类
    filter_backends = [DjangoFilterBackend]  # 采用哪个过滤器
    filterset_fields = ['goods_name', 'goods_price']  # 进行查询的字段


class TypeViewSet(viewsets.ModelViewSet):
    """
    返回具体的查询内容
    """
    queryset = GoodsType.objects.all()
    serializer_class = GoodsTypeSerializer


def ajax_goods_list(request):
    return render(request, "store/ajax_goods_list.html")


def delete_order(request):
    referer = request.META.get("HTTP_REFERER")
    order_id = request.GET.get("order_id")
    order = Order.objects.filter(id=int(order_id))  #
    orderlist = order.orderdetail_set.all()
    print(order)
    print(orderlist)
    # order.delete()
    return HttpResponseRedirect(referer)


from CeleryTask.tasks import add
from django.http import JsonResponse


def get_add(request):
    add.delay(2, 3)
    return JsonResponse({"status": 200})


from django.views.decorators.cache import cache_page


@cache_page(60*15)  # 对当前视图进行缓存，缓存的寿命是15分钟
def small_white_view(request):
    return HttpResponse("小白的视图")



