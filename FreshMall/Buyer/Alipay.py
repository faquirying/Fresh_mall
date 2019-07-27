# import sys
# sys.path.append(r"D:\Anaconda3\envs\DjangoPath\Lib\site-packages")
# sys.path.append(r"d:\anaconda3\envs\djangopath\lib\site-packages (from python-alipay-sdk) (3.7.2)")
from alipay import AliPay

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0q4vWV7917wtVHlVNEELuqVihAThPKU6sa/8u0JXjVHt2qQ3oJBFJ9AfOclzzqfuqC6tjvweIzc0R/wO0AA47XqD8MIP/83DYv3E1t3A2WBdAwEjVX+uVRKDl00vPlXrmB1hsoqWgrv1L2gpPZlmFNDc7yTKYgGsChEE3Z3x6r5DjfeiwENb3akKPxLa3qikJfHaYVtCHvDze6XXoPn/YDh6+7sfhpmUuA5XnZfNy/8tajTzGhvls90hojRKO5nn4pSXm79190ZHGO0GSxyUVMIFwez7/VEfYtejh4lbDH+FF9LgY1Dl09UmAYKSjWMjuA7P16u+D6dNublXhlNOqQIDAQAB
-----END PUBLIC KEY-----"""

app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDSri9ZXv3XvC1UeVU0QQu6pWKEBOE8pTqxr/y7QleNUe3apDegkEUn0B85yXPOp+6oLq2O/B4jNzRH/A7QADjteoPwwg//zcNi/cTW3cDZYF0DASNVf65VEoOXTS8+VeuYHWGyipaCu/UvaCk9mWYU0NzvJMpiAawKEQTdnfHqvkON96LAQ1vdqQo/EtreqKQl8dphW0Ie8PN7pdeg+f9gOHr7ux+GmZS4Dledl83L/y1qNPMaG+Wz3SGiNEo7mefilJebv3X3RkcY7QZLHJRUwgXB7Pv9UR9i16OHiVsMf4UX0uBjUOXT1SYBgpKNYyO4Ds/Xq74Pp025uVeGU06pAgMBAAECggEAMYZ83vdzmLlFtqvnGaeIyFGEfSBgik8VIxwJv0NzLWdrEJC1+uqvNxK3pG/050mW0rZWWlxuAT1C7wETwlWrDDhWt8wG0s1d9vFMym3Knc8HTmOAGOMw6hK2GGUui+rKvTF6++uUQhtJIeHMgAyFcLNAnH77jFp0RNGHYUl1ywaNzMrNPTQqY6YsSB/zHC9yxBhniiLu5Xk1av/As/XUAxrrT2jdzy6YyZ5pJsutcqpVSZP8XWdWv63EY0SleW/0GFHTJk7oni7kdgFKcWYQF566VgzYJpycSqZm3pafKcsghGEVjIkDrfHDEzt6GFsE38M5vJng1BP6Ouks9LcQAQKBgQDrHkdiTuC04VJW3XSm3lN6x6oTcljVPdS/Ghq4qJsVfETm4FSjIC4qkf3lCukb01Q1QQB+uenMTiOIT+/ijyYGRDO0rHUCZeCZMzLtuDc9xyK2PBGHf568ZRo0GKj/0JqPbQonMuUNwijqD3RYu6h1Z09SicbDtvwsNDHxsCmrAQKBgQDlZEd/jcbkZ6Qre7xkYzGm7uT6ou3vpck8/DGxmj5pU5oBrGWAfK3zAH15kLU0eY1b3SURe2tKxBEzvdxv8o1hIdpMYiVY3PIdWUBz7A3CRO0lGoaSk55U6Y430QY2vIEewJeSYN3mHGqlnM07UUuX1h0VjRyN57oDurZ+CFhrqQKBgEkZqOgPzh1u0MLhJ5uaFCpgWaiiLKxgBP1FiHlRMqaDdIizxpzRLIlfyqijs8ZK9it4gkbkVqSGxtVixRqTlybrnYfW9qpAMoxvNq5iUAqNF2XBV1Hhg+DfLj50TFb87JEbPcTiNgUJEN903p+X+NBHxonK/FltUwoLUFvsgYgBAoGACvZr5FCmPKwnUFyteC61ZMDt+Hxo2pcVsvBqf45bhTUVmxbeEvHibkaLuI+N2WAlvUooR1mamwwbtllQe5kf4JB5mkTmfASzHWvyhJe3YJ1ip+9IlyCu5Gf0//3hSiRgF1Qk6j3u3NxmzFteA4OzFSKKaUlBIBb+8Mavif5kG2ECgYEA51CnuUVsbWyN0uVnmNL++kvLxEeTyzEwW9K+ItA2W9K2DrCQ/lgKzgk2BwLjCWbSzHkgoTvzhhdnZJ/ELHG6xDVFy7zIjQPHNLE6AyyBM+3XR+Id2GUURgqZmfsZEHohbbri3gHFBkRPCRmBSPQo58KW0jEYvHBvKRV0VqDleE0=
-----END RSA PRIVATE KEY-----"""


# 实例化支付应用
alipay = AliPay(
    appid = "2016101000652488",
    app_notify_url = None,
    app_private_key_string = app_private_key_string,
    alipay_public_key_string = alipay_public_key_string,
    sign_type = "RSA2"
)

# 发起支付请求
order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no = "3307",
    total_amount=str(300000),
    subject="生鲜交易",
    return_url=None,
    notify_url=None
)

print("https://openapi.alipaydev.com/gateway.do?"+order_string)

