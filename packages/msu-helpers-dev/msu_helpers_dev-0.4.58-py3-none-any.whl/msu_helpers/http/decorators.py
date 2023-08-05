from django.views.decorators.http import require_http_methods, require_GET, require_POST

__all__ = ('get', 'post', 'http_method')

http_method = require_http_methods
get = require_GET
post = require_POST


def from_query(query_model_cls):
    def wrapper(view_func):
        def wrapped(request, *args, **kw):
            request.model = query_model_cls.deserialize(request.GET)
            return view_func(request, *args, **kw)
        return wrapped
    return wrapper
