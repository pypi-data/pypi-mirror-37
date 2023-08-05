from django.views.decorators.http import require_http_methods, require_GET, require_POST
from ..interface.query_models.base import *

__all__ = ('get', 'post', 'http_method', 'from_query')

http_method = require_http_methods
get = require_GET
post = require_POST


def from_query(query_model_cls):
    def wrapper(view_func):
        def wrapped(request, *args, **kw):
            if isinstance(query_model_cls, BaseQueryModel):
                request.model = query_model_cls.deserialize(request.GET)
                return view_func(request, *args, **kw)
            raise TypeError(f'Invalid query model class {query_model_cls.__name__}. '
                            f'It should be inherited from "BaseQueryModel"')
        return wrapped
    return wrapper
