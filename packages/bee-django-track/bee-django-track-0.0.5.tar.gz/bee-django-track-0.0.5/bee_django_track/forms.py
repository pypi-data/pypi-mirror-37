# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms

from .models import UserTrackRecord, ContentType


class UserTrackRecordForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(queryset=ContentType.objects.filter(is_add=True), label='类型', required=True)

    class Meta:
        model = UserTrackRecord
        fields = ['content_type', 'title', 'info']
