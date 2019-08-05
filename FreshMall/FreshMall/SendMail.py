import smtplib  # 登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText  # 负责构建邮件格式

subject = "天才2组团建第二弹"
content = "本周六晚102集合，进行天才2组团建第二弹，欢迎大(dou)家(tm)参(de)与(lai)!"
sender = "215558997@qq.com"
recver = """1305229816@qq.com,
944612390@qq.com,
923307639@qq.com,
1104926841@qq.com,
361153665@qq.com,
260376308@qq.com"""

password = "idjsflwsglutcace"

message = MIMEText(content, "plain", "utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
smtp.login(sender, password)
smtp.sendmail(sender, recver.split(",\n"), message.as_string())
smtp.close()
