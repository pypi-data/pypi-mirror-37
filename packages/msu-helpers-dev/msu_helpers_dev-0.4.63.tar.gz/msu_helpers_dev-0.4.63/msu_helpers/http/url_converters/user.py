from ...interface.query_models.user import *

__all__ = ('UserSearchModelConverter',)


# deprecated
class UserSearchModelConverter:
    regex = '\?(first_name=([\wА-Яа-я]+))?&?(last_name=([\wА-Яа-я]+))?&?(group_name=([\wА-Яа-я\-\d]{0,10}))?&?'

    def to_python(self, value):
        return UserSearchModel()

    # def to_url(self, value):
    #     return '%04d' % value
