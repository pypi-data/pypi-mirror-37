#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'bee'
import json
from django.conf import settings
from django.apps import apps
from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import Message, SendRecord


class JSONResponse(HttpResponse):
    def __init__(self, obj):
        if isinstance(obj, dict):
            _json_str = json.dumps(obj)
        else:
            _json_str = obj
        super(JSONResponse, self).__init__(_json_str, content_type="application/json;charset=utf-8")


def get_message(identity=None):
    message = None
    if identity:
        try:
            message = Message.objects.get(identity=identity)
        except:
            message = None
    return message


# def get_user_model():
#     if settings.MESSAGE_USER_TABLE in ["", None]:
#         user_model = User
#     else:
#         app_name = settings.MESSAGE_USER_TABLE.split(".")[0]
#         model_name = settings.MESSAGE_USER_TABLE.split(".")[1]
#         app = apps.get_app_config(app_name)
#         user_model = app.get_model(model_name)
#     return user_model
#
#
# # 获取登录用户
# def get_login_user(request):
#     if settings.MESSAGE_USER_TABLE in ["", None]:
#         return request.user
#
#     token = request.COOKIES.get('cookie_token', '')
#     # 没有登录
#     if not token:
#         return None
#
#     try:
#         user_table = get_user_model()
#         user = user_table.objects.get(token=token)
#         return user
#     except:
#         return None


# 获取自定义user的自定义name
def get_user_name(user):
    try:
        return getattr(user, settings.USER_NAME_FIELD)
    except:
        return None





# 获取学生未读信息的数量
def get_user_new_message_count(user, message_identity=None):
    if not user or not user.is_authenticated():
        return 0
    message = get_message(message_identity)
    records = SendRecord.objects.filter(to_user=user, is_view=False)
    if message:
        records = records.filter(message=message)
    return records.count()


# context
def get_context_user_new_message_count(request):
    context = {
        'context_user_new_message_count': get_user_new_message_count(request.user),
    }
    return context
