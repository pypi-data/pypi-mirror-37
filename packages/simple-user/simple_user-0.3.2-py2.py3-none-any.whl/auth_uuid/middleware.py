from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = get_user_model(
            ).objects.retrieve_remote_user_by_cookie(
                request.COOKIES)
