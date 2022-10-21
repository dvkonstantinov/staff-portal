from django.contrib.auth.views import (LogoutView, LoginView,
                                       PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView,
                                       PasswordResetDoneView)
from django.urls import path, reverse_lazy

from .forms import UserLoginForm
from .views import CustomPasswordChangeView, SignUpView, \
    email_verification_done, \
    CustomPasswordResetView, email_verification, CustomLoginView

app_name = 'authapp'

urlpatterns = [
    path('logout/',
         LogoutView.as_view(template_name='authapp/logged_out.html'),
         name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verification/', email_verification, name='email_verification'),
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
    path(
        'password_reset/done/',
        PasswordResetView.as_view(
            template_name='authapp/password_reset_done.html'),
        name='password_reset_done'
    ),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='authapp/password_reset_confirm.html'),
         name='password_reset_confirm'
         ),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='authapp/password_reset_complete.html'),
         name='password_reset_complete'
         )
]
