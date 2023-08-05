from .base import *

__all__ = ('UserSearchModel',)


class UserSearchModel(Base):
    class Meta:
        __str_fields__ = ('p_first_name', 'p_last_name', 'p_group_code')
