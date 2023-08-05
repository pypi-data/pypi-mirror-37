import json
from json import JSONDecodeError


class HttpRequestBodySerializer:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            request.data = json.loads(request.body)
            request.is_valid = True
        except JSONDecodeError as e:
            request.is_valid = False
            request.data = f'{e}. Invalid data.'

        response = self.get_response(request)

        return response
