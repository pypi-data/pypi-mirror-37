#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .models import Group, Language
from .managers import UserManager

__all__ = ('AuthUser', 'UserAdmin')


class AuthUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    group = models.ForeignKey(Group, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)
    birthday = models.DateField(auto_now_add=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/users/profile_pics', null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    lang = models.ForeignKey(Language, related_name='users', on_delete=models.DO_NOTHING, null=True, blank=True)
    activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, editable=False)

    objects = UserManager()

    _serializer = None

    __fields__ = ('first_name', 'last_name', 'group_id', 'about',
                  'profile_pic', 'email', 'lang_id', 'activated',)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = '_User'

    def __str__(self):
        return f'{self.email} - {self.first_name} {self.last_name}'

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def serialized(self) -> dict:
        return self.serializer.data

    @property
    def serializer(self):
        if self._serializer is None:
            self._serializer = self._get_serializer(self)
        return self._serializer

    @classmethod
    def _get_serializer(cls, data):
        from . import serializers
        serializer_class = serializers.get('User')
        if isinstance(data, cls):
            return serializer_class(data)
        elif isinstance(data, dict):
            return serializer_class(data=data)
        else:
            raise TypeError('"data" should be dict or Group')


class UserAdmin(admin.ModelAdmin):
    exclude = ('password', 'last_login', 'user_permissions', 'groups')
