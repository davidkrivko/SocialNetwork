from rest_framework_simplejwt.authentication import JWTAuthentication

from network_config.redis import add_online_flag


class UpdateUserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            user = JWTAuthentication().authenticate(request)[0]
        except:
            response = self.get_response(request)
            return response

        if user.is_authenticated:
            add_online_flag(user.username)

        response = self.get_response(request)
        return response
