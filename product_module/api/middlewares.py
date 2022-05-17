import base64
import ast
from rest_framework.response import Response
from website.models import User

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        encoded_string = request.POST.get('token')
        # decoded_base64_bytes = encoded_string.encode("ascii")
        # decoded_base64_bytes = base64.b64decode(decoded_base64_bytes)
        # decoded_base64_string = decoded_base64_bytes.decode("ascii")

        # hasher = decoded_base64_string.split('$')[1]

        # user = User.objects.get(password.split('$')[3]=hasher)

        response = self.get_response(request)
        # r = response.content.decode("ascii")
        # res = ast.literal_eval(r)
        # encoded_string = res["encoded"]

        return response
