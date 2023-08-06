#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from .models import UserTrackRecord, ContentType


# 保存足迹
def add_user_track_record(user, content_type_identity=None, content_id=None, title=None, info=None, created_by=None):
    content_type = None
    record = UserTrackRecord()
    if content_type_identity:
        try:
            content_type = ContentType.objects.get(identity=content_type_identity)
            record.content_id = content_id
        except:
            content_type = None
    try:
        record.user = user
        record.content_type = content_type
        record.title = title
        record.info = info
        record.created_by = created_by
        record.save()
        return
    except Exception as e:
        print('bee_django_track->add_user_track_record->error:' + e.__str__())
        return
