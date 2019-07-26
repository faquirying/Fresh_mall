from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect

from Buyer.models import *
from Store.views import set_password

# Create your views here.
def loginValid(fun):
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
    return render(request,"buyer/index.html")


def login(request):
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
    response = HttpResponseRedirect("/buyer/login")
    for key in request.COOKIES:
        response.delete_cookie(key)
    del request.session["username"]
    return response