#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import json
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model

from .decorators import cls_decorator, func_decorator
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Sum, Count
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Message, SendRecord
from .forms import MessageForm
from .utils import get_user_name, JSONResponse

User = get_user_model()


# Create your views here.
# =======course=======
def test(request):
    from utils import send_message
    from django.contrib.auth.models import User
    to_user = User.objects.get(id=1)
    res = send_message(to_user=to_user, from_user=to_user, message_identity='to_user', title='test', url=None)
    return HttpResponse('OK')


@method_decorator(cls_decorator(cls_name='MessageList'), name='dispatch')
class MessageList(ListView):
    template_name = 'bee_django_message/message/message_list.html'
    context_object_name = 'message_list'
    paginate_by = 20
    queryset = Message.objects.all()


@method_decorator(cls_decorator(cls_name='MessageDetail'), name='dispatch')
class MessageDetail(DetailView):
    model = Message
    template_name = 'bee_django_message/message/message_detail.html'
    context_object_name = 'message'


@method_decorator(cls_decorator(cls_name='MessageCreate'), name='dispatch')
class MessageCreate(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'bee_django_message/message/message_form.html'


@method_decorator(cls_decorator(cls_name='MessageUpdate'), name='dispatch')
class MessageUpdate(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'bee_django_message/message/message_form.html'


@method_decorator(cls_decorator(cls_name='MessageDelete'), name='dispatch')
class MessageDelete(DeleteView):
    model = Message
    success_url = reverse_lazy('bee_django_message:message_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# 发送记录
@method_decorator(cls_decorator(cls_name='UserRecordList'), name='dispatch')
class UserRecordList(ListView):
    template_name = 'bee_django_message/record/user_record_list.html'
    context_object_name = 'record_list'
    paginate_by = 20
    queryset = None

    def get_user(self):
        user_id = self.kwargs["user_id"]
        if user_id in [None, "0"]:
            return None
        user = User.objects.get(id=user_id)
        return user

    def get_queryset(self):
        user = self.get_user()
        self.queryset = SendRecord.objects.filter(to_user=user)
        return self.queryset

    def get_context_data(self, **kwargs):
        user = self.get_user()
        context = super(UserRecordList, self).get_context_data(**kwargs)
        context['user'] = user
        return context


#
# @method_decorator(cls_decorator(cls_name='RecordDetail'), name='dispatch')
# class RecordDetail(DetailView):
#     model = SendRecord
#     template_name = 'bee_django_message/message/message_detail.html'
#     context_object_name = 'record'


@method_decorator(cls_decorator(cls_name='UserRecordClick'), name='dispatch')
class UserRecordClick(TemplateView):
    def post(self, request, *args, **kwargs):
        record_id = request.POST.get("record_id")
        record = SendRecord.objects.get(id=record_id)
        record.is_view = True
        record.save()
        return JSONResponse(json.dumps({"url": record.url}, ensure_ascii=False))


class UserRecordAllClick(TemplateView):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            pass
        except:
            res = {"error": 1, "message": "参数错误"}
            return JSONResponse(json.dumps(res, ensure_ascii=False))
        record_list = SendRecord.objects.filter(to_user=user,is_view=False)
        for record in record_list:
            record.is_view = True
            record.save()
        res = {"error": 0, "message": "操作成功"}
        return JSONResponse(json.dumps(res, ensure_ascii=False))
