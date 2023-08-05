#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django.conf import settings
from django.contrib.auth.models import User

from .models import Message, SendRecord
from utils import get_message

# def get_user(request):
#     return get_login_user(request)







# 消息状态改为已读信息
# def change_message_stutas(message_record_id):
#     try:
#         record = SendRecord.objects.get(id=message_record_id)
#         record.is_view = True
#         record.save()
#     except:
#         return False
#
# # django前台显示本地时间
# def filter_local_datetime(_datetime):
#     return _datetime