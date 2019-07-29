from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.models import *
from Store.views import set_password

from alipay import AliPay

import time

# Create your views here.
def loginValid(fun):
    """
    登录校验
    """
    def inner(request,*args,**kwargs):
        c_user = request.COOKIES.get("username")
        s_user = request.session.get("username")
        if c_user and s_user and c_user == s_user:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/buyer/login")
    return inner


def base(request):
    return render(request,"buyer/base.html")


@ loginValid
def index(request):
    """
    前端首页
    """
    result_list = []  # 定义一个容器来存放结果
    goods_type_list = GoodsType.objects.all()  # 查询所有的类型
    for goods_type in goods_type_list:  # 循环类型
        goods_list = goods_type.goods_set.values()[:4]  # 查询4条数据
        if goods_list:  # 如果类型对应的值不为空
            goodsType = {
                "id":goods_type.id,
                "name": goods_type.name,
                "description": goods_type.description,
                "picture": goods_type.picture,
                "goods_list": goods_list
            }  # 构建输出结果
            #  查询类型当中有数据的数据
            result_list.append(goodsType)
    return render(request,"buyer/index.html",locals())


@loginValid
def goods_list(request):
    """
    列表详情页
    """
    goodsList = []
    type_id = request.GET.get("id")
    # 获取类型
    goods_type = GoodsType.objects.filter(id = int(type_id)).first()
    print(goods_type)
    if goods_type:
        # 查询所有上架的产品
        goodsList = goods_type.goods_set.filter(goods_status=1)
        print(goodsList)
    return render(request,"buyer/goods_list.html",locals())


def login(request):
    """
    前端登录页面
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        if username and password:
            user = Buyer.objects.filter(username=username).first()
            if user and user.password == set_password(password):
                response = HttpResponseRedirect("/buyer/index")
                # 登录校验
                response.set_cookie("username",user.username)
                request.session["username"] = user.username
                # 方便其他查询
                response.set_cookie("user_id",user.id)
                return response
    return render(request,"buyer/login.html")


def register(request):
    """
    前端注册页
    """
    if request.method == "POST":
        # 获取前端post请求的数据
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        buyer = Buyer()
        buyer.username = username
        buyer.password = set_password(password)
        buyer.email = email
        buyer.save()
        return HttpResponseRedirect("/buyer/login")
    return render(request,"buyer/register.html")


def logout(request):
    """
    退出登录
    """
    response = HttpResponseRedirect("/buyer/login")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response


def cart(request):
    """
    购物车
    """
    return render(request,"buyer/cart.html")


def pay_order(request):
    money = request.GET.get("money")  # 获取订单的金额
    order_id = request.GET.get("order_id")  # 获取订单id
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0q4vWV7917wtVHlVNEELuqVihAThPKU6sa/8u0JXjVHt2qQ3oJBFJ9AfOclzzqfuqC6tjvweIzc0R/wO0AA47XqD8MIP/83DYv3E1t3A2WBdAwEjVX+uVRKDl00vPlXrmB1hsoqWgrv1L2gpPZlmFNDc7yTKYgGsChEE3Z3x6r5DjfeiwENb3akKPxLa3qikJfHaYVtCHvDze6XXoPn/YDh6+7sfhpmUuA5XnZfNy/8tajTzGhvls90hojRKO5nn4pSXm79190ZHGO0GSxyUVMIFwez7/VEfYtejh4lbDH+FF9LgY1Dl09UmAYKSjWMjuA7P16u+D6dNublXhlNOqQIDAQAB
    -----END PUBLIC KEY-----"""

    app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDSri9ZXv3XvC1UeVU0QQu6pWKEBOE8pTqxr/y7QleNUe3apDegkEUn0B85yXPOp+6oLq2O/B4jNzRH/A7QADjteoPwwg//zcNi/cTW3cDZYF0DASNVf65VEoOXTS8+VeuYHWGyipaCu/UvaCk9mWYU0NzvJMpiAawKEQTdnfHqvkON96LAQ1vdqQo/EtreqKQl8dphW0Ie8PN7pdeg+f9gOHr7ux+GmZS4Dledl83L/y1qNPMaG+Wz3SGiNEo7mefilJebv3X3RkcY7QZLHJRUwgXB7Pv9UR9i16OHiVsMf4UX0uBjUOXT1SYBgpKNYyO4Ds/Xq74Pp025uVeGU06pAgMBAAECggEAMYZ83vdzmLlFtqvnGaeIyFGEfSBgik8VIxwJv0NzLWdrEJC1+uqvNxK3pG/050mW0rZWWlxuAT1C7wETwlWrDDhWt8wG0s1d9vFMym3Knc8HTmOAGOMw6hK2GGUui+rKvTF6++uUQhtJIeHMgAyFcLNAnH77jFp0RNGHYUl1ywaNzMrNPTQqY6YsSB/zHC9yxBhniiLu5Xk1av/As/XUAxrrT2jdzy6YyZ5pJsutcqpVSZP8XWdWv63EY0SleW/0GFHTJk7oni7kdgFKcWYQF566VgzYJpycSqZm3pafKcsghGEVjIkDrfHDEzt6GFsE38M5vJng1BP6Ouks9LcQAQKBgQDrHkdiTuC04VJW3XSm3lN6x6oTcljVPdS/Ghq4qJsVfETm4FSjIC4qkf3lCukb01Q1QQB+uenMTiOIT+/ijyYGRDO0rHUCZeCZMzLtuDc9xyK2PBGHf568ZRo0GKj/0JqPbQonMuUNwijqD3RYu6h1Z09SicbDtvwsNDHxsCmrAQKBgQDlZEd/jcbkZ6Qre7xkYzGm7uT6ou3vpck8/DGxmj5pU5oBrGWAfK3zAH15kLU0eY1b3SURe2tKxBEzvdxv8o1hIdpMYiVY3PIdWUBz7A3CRO0lGoaSk55U6Y430QY2vIEewJeSYN3mHGqlnM07UUuX1h0VjRyN57oDurZ+CFhrqQKBgEkZqOgPzh1u0MLhJ5uaFCpgWaiiLKxgBP1FiHlRMqaDdIizxpzRLIlfyqijs8ZK9it4gkbkVqSGxtVixRqTlybrnYfW9qpAMoxvNq5iUAqNF2XBV1Hhg+DfLj50TFb87JEbPcTiNgUJEN903p+X+NBHxonK/FltUwoLUFvsgYgBAoGACvZr5FCmPKwnUFyteC61ZMDt+Hxo2pcVsvBqf45bhTUVmxbeEvHibkaLuI+N2WAlvUooR1mamwwbtllQe5kf4JB5mkTmfASzHWvyhJe3YJ1ip+9IlyCu5Gf0//3hSiRgF1Qk6j3u3NxmzFteA4OzFSKKaUlBIBb+8Mavif5kG2ECgYEA51CnuUVsbWyN0uVnmNL++kvLxEeTyzEwW9K+ItA2W9K2DrCQ/lgKzgk2BwLjCWbSzHkgoTvzhhdnZJ/ELHG6xDVFy7zIjQPHNLE6AyyBM+3XR+Id2GUURgqZmfsZEHohbbri3gHFBkRPCRmBSPQo58KW0jEYvHBvKRV0VqDleE0=
    -----END RSA PRIVATE KEY-----"""

    # 实例化支付应用
    alipay = AliPay(
        appid="2016101000652488",
        app_notify_url=None,
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2"
    )

    # 发起支付请求
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),
        subject="生鲜交易",
        return_url="http://127.0.0.1:8000/buyer/pay_result/",  # 支付完成要跳转的本地路由
        notify_url="http://127.0.0.1:8000/buyer/pay_result/"  # 支付完成要跳转的本地异步路由
    )

    order = Order.objects.get(order_id=order_id)
    order.order_status = 2
    order.save()

    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)  # 跳转支付路由


def pay_result(request):
    """
    支付宝支付成功自动用get请求返回的参数
    # 编码
    charset=utf-8
    # 订单号
    out_trade_no=10002
    # 订单类型
    method=alipay.trade.page.pay.return
    # 订单金额
    total_amount=1000.0
    """
    return render(request,"buyer/pay_result.html")


def detail(request):
    goods_id = request.GET.get("id")
    if goods_id:
        goods = Goods.objects.filter(id=int(goods_id)).first()
        if goods:
            return render(request,"buyer/detail.html",{"goods":goods})
    return HttpResponse("无法找到商品详情页")


def setOrderId(user_id,goods_id,store_id):
    """
    生成订单号：时间+用户id + 商品id + 店铺id
    """
    strtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
    return strtime + user_id + goods_id + store_id


def order(request):
    if request.method == "POST":
        # post 数据
        count = int(request.POST.get("count"))
        goods_id = request.POST.get("goods_id")
        print(count)
        # cookie的数据
        user_id = request.COOKIES.get("user_id")
        # 数据库的数据
        goods = Goods.objects.get(id=goods_id)
        store_id = goods.store_id.id
        price = goods.goods_price
        # 向订单表提交数据
        order = Order()
        order.order_id = setOrderId(str(user_id),str(goods_id),str(store_id))
        order.goods_count = count
        order.order_user = Buyer.objects.get(id = user_id)
        order.order_price = count * price
        order.order_status = 1
        order.save()
        # 向订单详细表提交数据
        order_detail = OrderDetail()
        order_detail.order_id = order
        order_detail.goods_id = goods_id
        order_detail.goods_name = goods.goods_name
        order_detail.goods_price = goods.goods_price
        order_detail.goods_number = count
        order_detail.goods_total = count * goods.goods_price
        order_detail.goods_store = store_id
        order_detail.goods_image = goods.goods_image
        order_detail.save()

        detail = [order_detail]

        return render(request,"buyer/order.html",locals())
    else:
        return HttpResponse('hhh')

