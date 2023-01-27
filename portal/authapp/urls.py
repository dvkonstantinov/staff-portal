from django.contrib.auth.views import (LogoutView, PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from .views import (CustomLoginView, CustomPasswordChangeView,
                    CustomPasswordResetView, email_verification,
                    email_verification_done, resend_email, signup_view)

app_name = 'authapp'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='authapp/logged_out.html'),
         name='logout'),
    path('signup/', signup_view, name='signup'),
    path('verification/', email_verification, name='email_verification'),
    path('resend-email/', resend_email, name='resend_email'),
    path('verification/<uidb64>/<token>/', email_verification_done,
         name='email_verification_done'),
    path(
        'login/',
        CustomLoginView.as_view(), name='login'
    ),
    path('password_change/', CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/done/',
         PasswordResetDoneView.as_view(
             template_name='authapp/password_change_done.html'),
         name='password_change_done'
         ),
    path(
        'password_reset/',
        CustomPasswordResetView.as_view(
            template_name='authapp/password_reset_form.html',
            success_url=reverse_lazy('authapp:password_reset_done')
        ),
        name='password_reset'
    ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='authapp/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path(
        'password_reset/done/',
        PasswordResetView.as_view(
            template_name='authapp/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='authapp/password_reset_complete.html'),
         name='password_reset_complete'
         )
]
