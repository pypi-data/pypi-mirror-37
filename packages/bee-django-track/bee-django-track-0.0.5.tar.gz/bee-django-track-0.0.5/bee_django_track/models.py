# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse


# 类别
class ContentType(models.Model):
    title = models.CharField(max_length=180, verbose_name='标题')
    identity = models.CharField(max_length=180, null=True, verbose_name='标识符', unique=True, help_text='此字段唯一')
    app_label = models.CharField(max_length=180, verbose_name='app名', null=True, blank=True)
    model = models.CharField(max_length=180, verbose_name='模块名', null=True, blank=True)
    user_field = models.CharField(max_length=180, verbose_name='用户字段名', null=True, blank=True)
    link = models.CharField(max_length=180, verbose_name='链接', null=True, blank=True)
    link_type = models.IntegerField(default=1)
    info = models.CharField(max_length=180, verbose_name='备注', null=True, blank=True)
    is_add = models.BooleanField(default=True, verbose_name='是否可添加')
    is_edit = models.BooleanField(default=True, verbose_name='是否可修改')

    class Meta:
        db_table = 'bee_django_track_content_type'
        app_label = 'bee_django_track'
        ordering = ['id']
        unique_together = ("app_label", 'model')

    def __unicode__(self):
        return self.title


# Create your models here.
class UserTrackRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户')
    title = models.CharField(max_length=180, verbose_name='标题')
    info = models.TextField(verbose_name='详情',null=True,blank=True)
    content_type = models.ForeignKey(ContentType, verbose_name='类型')
    content_id = models.IntegerField(ContentType, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='由谁添加', null=True,
                                   related_name='create_by_user')
    created_at = models.DateTimeField(auto_now_add=True)  # 时间

    class Meta:
        db_table = 'bee_django_track_record'
        app_label = 'bee_django_track'
        ordering = ["-created_at"]
        permissions = (
            ('view_user_leave', '可以查看学生请假类足迹'),
            ('view_crm_fee', '可以查看缴费类足迹'),
            ('view_crm_referral', '可以查看转介类足迹'),
            ('add_track_other', '可以添加其他类足迹'),
            ('view_track_other', '可以查看其他类足迹'),
        )


    def __unicode__(self):
        return ("title:" + self.title)

    def get_link(self):
        if not self.content_type.link:
            return reverse("bee_django_track:record_detail", kwargs={"pk":self.pk})
        if self.content_type.link_type == 1:
            return self.content_type.link + self.content_id.__str__()
        return
