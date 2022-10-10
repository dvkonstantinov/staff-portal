from django.contrib.auth.views import (LogoutView, LoginView,
                                       PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordResetDoneView)
from django.urls import path, reverse_lazy

from .forms import UserLoginForm
from .views import CustomPasswordChangeView, SignUpView, verify_email, \
    CustomPasswordResetView

app_name = 'users'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', verify_email, name='verify_email'),
    path(
        'login/',
        LoginView.as_view(template_name='users/login.html',
                          authentication_form=UserLoginForm),
        name='login'
    ),
    path(
        'password_change/',
        CustomPasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'
    ),
    path('password_change/done/',
         PasswordResetDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'
         ),
    path(
        'password_reset/',
        CustomPasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetView.as_view(
            template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'
         ),
]
