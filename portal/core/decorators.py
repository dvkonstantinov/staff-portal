from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def adminuser_required(view_func=None,
                       redirect_field_name=REDIRECT_FIELD_NAME,
                       login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_admin and u.verified,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
