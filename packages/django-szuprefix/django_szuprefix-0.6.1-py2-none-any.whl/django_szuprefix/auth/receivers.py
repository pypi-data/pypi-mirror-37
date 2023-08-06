# -*- coding:utf-8 -*-
from django.dispatch import receiver
from .signals import to_bind_user
from ..utils.modelutils import move_relation

@receiver(to_bind_user)
def bind_user(sender, **kwargs):
    old_user = kwargs['old_user']
    new_user = kwargs['new_user']
    move_relation(old_user, new_user)
    old_user.is_active = False
    old_user.save()
