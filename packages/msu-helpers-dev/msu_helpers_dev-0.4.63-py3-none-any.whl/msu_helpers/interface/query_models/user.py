from .base import *

__all__ = ('UserSearchModel',)


class UserSearchModel(BaseQueryModel):
    __str_fields__ = ('first_name', 'last_name', 'group_code')

    def __init__(self):
        self.first_name: str = str()
        self.last_name: str = str()
        self.group_code: str = str()
