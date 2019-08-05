from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置celery执行的环境变量，执行django项目的配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CeleryTask.settings")

# 创建celery应用
app = Celery('art_project')  # celery应用的名称
app.config_from_object('django.conf:settings')  # 加载的配置文件

# 如果在工程的应用中创建了task.py模块，那么Celery应用就会自动去检索创建的任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)