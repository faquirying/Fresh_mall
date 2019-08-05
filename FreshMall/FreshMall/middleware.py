# coding:utf-8
from django.utils.deprecation import MiddlewareMixin  # 中间件的元类，所有自定义的中间件自定义时都必须实现方法重写
from django.http import HttpResponse


class MiddlewareTest(MiddlewareMixin):
    def process_request(self,request):
        """
        :return: 视图没有处理的请求
        """
        username = request.GET.get("username")
        if username and username == "lb":
            return HttpResponse("404!")

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     """
    #     :param request: 视图没有处理的请求
    #     :param view_func: 视图函数
    #     :param view_args:  视图函数的参数，元组格式
    #     :param view_kwargs: 视图函数的参数，字典格式
    #     """
    #     print("这是process_view")
    #
    # def process_exception(self, request, exception):
    #     """
    #     :param request: 视图处理中的请求
    #     :param exception: 错误
    #     :return:
    #     """
    #     print("这是process_exception")
