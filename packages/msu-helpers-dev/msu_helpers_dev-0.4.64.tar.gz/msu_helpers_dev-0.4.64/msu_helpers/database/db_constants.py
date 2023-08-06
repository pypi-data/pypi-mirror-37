#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = ['Language', 'UserDefaults', 'ArticleDefaults', ]


class Language:
    EN_US = 'en-us'
    RU_RU = 'ru-ru'


class Utils:
    DATETIME_FORMAT = '%xT%X'


class UserDefaults:
    id = 0
    first_name = 'Funny'
    last_name = 'Bunny'
    study_group = 'БНБО-01-15'
    about = None
    profile_pic = None
    email = None
    password = None
    lang = Language.RU_RU
    activated = False
    is_staff = False

    @property
    def birthday(self):
        return datetime.utcnow().strftime(Utils.DATETIME_FORMAT)


class ArticleDefaults:
    id = 0
    body = None
    user = None

    @property
    def timestamp(self):
        return datetime.utcnow().strftime(Utils.DATETIME_FORMAT)


if __name__ == '__main__':
    pass
