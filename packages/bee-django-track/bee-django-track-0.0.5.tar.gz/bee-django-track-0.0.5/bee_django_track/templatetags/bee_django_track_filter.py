#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django import template
from django.conf import settings
from django.shortcuts import reverse

from bee_django_track.utils import get_user_name

register = template.Library()


# 求两个值的差的绝对值
@register.filter
def get_difference_abs(a, b):
    return abs(a - b)


# 获取学生姓名，及详情链接
@register.filter
def get_name_detail(user, show_detail=True):
    if not user:
        return None
    user_name = get_user_name(user)
    if not show_detail:
        return user_name
    if settings.USER_DETAIL_EX_LINK:
        link = "<a href='" + settings.USER_DETAIL_EX_LINK + user.id.__str__() + "/'>" + user_name + "</a>"
    else:
        link = user_name
    return link


@register.simple_tag
def get_record_link(cookie_user, record):
    if record.content_type.identity == 'user_leave':
        # and cookie_user.has_perm('bee_django_user.view_user_leave_record'):
        return record.get_link
    elif record.content_type.identity == 'crm_fee' and cookie_user.has_perm('bee_django_crm.view_crm_preuser_fee'):
        return record.get_link
    elif record.content_type.identity == 'crm_referral':
        # and cookie_user.has_perm('bee_django_trace.view_crm_referral'):
        return record.get_link
    elif record.content_type.identity == 'track_other':
        # and cookie_user.has_perm('bee_django_trace.view_track_other'):
        return record.get_link
