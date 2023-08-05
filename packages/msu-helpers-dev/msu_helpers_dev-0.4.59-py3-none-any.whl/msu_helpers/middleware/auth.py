import json
from json import JSONDecodeError


class BearerTokenAuth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # TODO Validate bearer auth token
        response = self.get_response(request)

        return response
