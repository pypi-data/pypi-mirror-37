#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypeVar, Generic
from django.http.response import JsonResponse
from ..http_constants import Status, Code

__all__ = ['CommonResponse']

T = TypeVar('T')
BASIC_TYPES = ['list', 'str', 'dict', 'int', 'float', 'tuple', 'bool', 'NoneType']


class CommonResponse(Generic[T]):

    def __init__(self, data: T, status: str = Status.SUCCESS, code: int = Code.SUCCESS, message: str = None,
                 sql: str = None):
        self.sql: str = sql
        self.status: str = status
        self.code: int = code
        self.message: str = message
        self.data: T = data

    @property
    def serialized(self) -> dict:
        return self._serialize()

    def _serialize(self) -> dict:
        if type(self.data).__name__ in BASIC_TYPES:
            data = self.data
        else:
            try:
                data = self.data.serialized
            except AttributeError:
                raise TypeError('Data should be serializable object or should have implemented property "serialized"')
        return {
            'status': self.status,
            'code': self.code,
            'message': self.message,
            'data': data,
            'sql': self.sql
        }

    @property
    def json_response(self) -> JsonResponse:
        return JsonResponse(self.serialized)

    @classmethod
    def success(cls, data: T = None, code: int = Code.SUCCESS, message: str = None, sql: str = None):
        return cls(data, Status.SUCCESS, code, message, sql).json_response

    @classmethod
    def created(cls, code: int = Code.CREATED, message: str = None, sql: str = None):
        return cls(None, Status.SUCCESS, code, message, sql).json_response

    @classmethod
    def failed(cls, code: int = Code.FAILED, message: str = None, sql: str = None):
        return cls(None, Status.FAILED, code, message, sql).json_response

    @classmethod
    def not_found(cls, message: str = 'Not Found', sql: str = None):
        return cls(None, Status.FAILED, Code.NOT_FOUND, message, sql).json_response

    @classmethod
    def unauthorized(cls, message: str = 'Unauthorized'):
        return cls(None, Status.FAILED, Code.UNAUTHORIZED, message).json_response

    @classmethod
    def forbidden(cls, message: str = 'Forbidden'):
        return cls(None, Status.FAILED, Code.FORBIDDEN, message).json_response

    @classmethod
    def server_error(cls, message: str = 'Internal server error'):
        return cls(None, Status.FAILED, Code.INTERNAL_SERVER_ERROR, message).json_response
