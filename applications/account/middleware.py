class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_blocked:
            from django.contrib.auth import logout
            from rest_framework.response import Response

            logout(request.user)
            return Response("доступ к приложению заблокирован")

        response = self.get_response(request)
        return response
