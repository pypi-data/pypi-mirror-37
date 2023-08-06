#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms
from .models import CoinType, UserCoinRecord


# ===== course contract======
class CoinTypeForm(forms.ModelForm):
    class Meta:
        model = CoinType
        fields = ['name', "identity", "coin", "info"]


class UserCoinRecordForm(forms.ModelForm):
    class Meta:
        model = UserCoinRecord
        fields = ["coin", "reason", 'coin_type']


class OtherCoinCreateForm(forms.ModelForm):
    user = forms.ModelChoiceField(label='选择学生', required=True, queryset=None)
    coin = forms.IntegerField(label='数量', required=True)
    reason = forms.CharField(label='原因', required=False)

    class Meta:
        model = UserCoinRecord
        fields = ["user", "coin", "reason"]

    def __init__(self, users, *args, **kwargs):
        super(OtherCoinCreateForm, self).__init__(*args, **kwargs)
        self.fields["user"] = forms.ModelChoiceField(queryset=users, label='选择学生', required=True)
