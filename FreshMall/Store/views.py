import hashlib
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import HttpResponseRedirect
from Store.models import *
from Buyer.models import *
# Create your views here.


def set_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    result = md5.hexdigest()
    return result


def register(request):
    """
    register注册
    返回注册页面
    进行注册数据保存
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = Seller.objects.filter(username=username).first()
            if not user:
                seller = Seller()
                seller.username = username
                seller.password = set_password(password)
                seller.nickname = username
                seller.save()
                return HttpResponseRedirect("/store/login/")
    return render(request,"store/register.html", locals())


def loginValid(fun):
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request,*args,**kwargs)
        else:
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
    response = render(request,"store/login.html")
    response.set_cookie("login_from", "login_page")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
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
                    store = Store.objects.filter(user_id=user.id).first() # 再查询店铺是否存在
                    if store:
                        response.set_cookie("has_store", store.id)
                    else:
                        response.set_cookie("has_store", "")
    return response


def out_login(request):
    response = HttpResponseRedirect('/store/login/')
    response.delete_cookie('username')
    return response


def base(request):
    return render(request,"store/base.html",locals())

# 添加店铺
@loginValid
def register_store(request):
    type_list = StoreType.objects.all()
    if request.method == "POST":
        post_data = request.POST  # 接收post数据
        store_name = post_data.get("store_name")
        store_descripton = post_data.get("store_descripton")
        store_phone = post_data.get("store_phone")
        store_money = post_data.get("store_money")
        store_address = post_data.get("store_address")

        user_id = int(request.COOKIES.get("user_id"))  # 通过cookie来得到user_id
        type_list = post_data.get("type")  # 通过request.post得到类型，但是是一个列表

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
        response = HttpResponseRedirect("/store/list_goods")
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
        goods.goods_description = goods_description
        goods.goods_date = goods_date
        goods.goods_safeDate = goods_safeDate
        goods.goods_image = goods_image
        goods.goods_type = GoodsType.objects.get(id=int(goods_type))
        goods.store_id = Store.objects.get(id = int(goods_store))
        goods.save()

        return HttpResponseRedirect("/store/list_goods/up/")
    return render(request, "store/add_goods.html",locals())

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
        goods_list = store.goods_set.filter(goods_name__contains=keywords,goods_status=state_num)  # 完成了模糊查询
    else:  # 如果关键词不存在，查询所有
        goods_list = store.goods_set.filter(goods_status=state_num)
    # 分页，每页3条
    paginator = Paginator(goods_list, 3)
    page = paginator.page(int(page_num))
    page_range = paginator.page_range
    print(page_range)
    # 返回分页数据
    return render(request, "store/list_goods.html", {"page": page, "page_range": page_range, "keywords": keywords,"state": state})

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
        goods = Goods.objects.filter(id = int(id)).first()
        if state == "delete":
            goods.delete()
        else:
            goods.goods_status = state_num
            goods.save()
    return HttpResponseRedirect(referer)


# 列表详情页
@loginValid
def descript_goods(request,goods_id):
    goods_data = Goods.objects.filter(id = goods_id).first()
    return render(request,"store/descript_goods.html",locals())


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
        goods = Goods.objects.get(id = int(goods_id))  # 获取当前商品
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
    order_list = OrderDetail.objects.filter(order_id__order_status=2,goods_store=store_id)
    return render(request,"store/order_list.html",locals())


