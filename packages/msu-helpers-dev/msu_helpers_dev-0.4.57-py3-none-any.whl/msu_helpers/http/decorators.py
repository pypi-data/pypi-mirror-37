from django.views.decorators.http import require_http_methods, require_GET, require_POST

__all__ = ('get', 'post', 'http_method')

http_method = require_http_methods
get = require_GET
post = require_POST
