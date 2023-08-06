# -*- coding:utf-8 -*-
__author__ = 'bee'
from django.dispatch import Signal
# 更新m币后，发送消息信号
send_message_single = Signal(providing_args=["user_coin_record"])