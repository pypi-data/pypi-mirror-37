#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['Status', 'Code', ]


class Status:
    SUCCESS: str = 'Success'
    FAILED: str = 'Failed'


class Code:
    SUCCESS: int = 200
    CREATED: int = 201
    FAILED: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    INTERNAL_SERVER_ERROR: int = 500
