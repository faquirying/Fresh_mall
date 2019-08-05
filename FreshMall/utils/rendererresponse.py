from rest_framework.renderers import JSONRenderer


class Customrenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        一种数据处理的方法
        :param data: 返回的数据
        :param accepted_media_type: 接受的类型
        :param renderer_context: 呈现的内容
        :return: 返回新的数据格式或者原数据
        """
        if renderer_context:  # 如果有数据请求过来
            if isinstance(data, dict):  # 判断返回的数据是否是一个字典
                msg = data.pop("msg", "请求成功")  # 如果是字典获取字典中的msg参数
                code = data.pop("code", 0)  # 如果是字典就获取字典中的code参数
            else:   # 非字典类型直接返回请求成功
                msg = '请求成功'
                code = 0
            ret = {
                "msg": msg,
                "code": code,
                "author": "我好帅！",
                "data": data
            }   # 重新构建返回数据形式
            return super().render(ret, accepted_media_type, renderer_context)   # 返回数据格式
        else:
            return super().render(data, accepted_media_type, renderer_context)  # 如果没有修改，返回原格式
