from __future__ import absolute_import
from FreshMall.celery import app   # 在安装成功celery框架之后，django新生成的模块


@app.task  # 将taskExample转换为一个任务
def taskExample():
    print('send email ok!')
    return 'send email ok!'


@app.task
def add(x=1, y=2):
    return x+y


@app.task
def DingTalk():
    url = "https://oapi.dingtalk.com/robot/send?access_token=48c30b6b81589fc087a6998787b1f3cd82e3624e0321e33d59ea4f903c2879e8"

    headers_data = {
        "msgtype": "text",
        "text": {
            "content": "everybody put you hands up in the air!!!"
        },
        "at":{
            "atMobilds": [

            ],
        },
        "isAtAll" : True
    }

    # sendData = json.dumps(request_data):
    # response = request.post(url,headers = headers, data=sendData)
    # content = response.json()
    # print(content)
