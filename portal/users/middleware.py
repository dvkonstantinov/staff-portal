from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class UpdateLastActivityMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.id).update(
                last_activity=timezone.now())
        response = self.get_response(request)

        return response
