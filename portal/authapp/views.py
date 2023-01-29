from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetView)
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode

from .forms import (CustomPasswordChangeForm, CustomPasswordResetForm,
                    UserLoginForm, UserRegistrationForm)
from .utils import account_activation_token, send_verification_email

User = get_user_model()


def signup_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST or None)
        if form.is_valid():
            user = form.save()
            is_success_mail = send_verification_email(user)
            if is_success_mail:
                return render(request, 'authapp/email_verification.html',
                              context={'user_email': user.email})
            else:
                form.add_error(None, 'Неудачная отправка Email. '
                                     'Попробуйте позднее')
                return render(request, 'authapp/signup.html',
                              context={'form': form})

    form = UserRegistrationForm(data=request.POST or None)
    return render(request, 'authapp/signup.html', context={'form': form})


def resend_email(request):
    try:
        email = request.POST['email']
    except KeyError:
        pass
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'message': 'error'}, status=404)

    is_success_mail = send_verification_email(user)
    if is_success_mail:
        return JsonResponse({'message': 'success'}, status=200)
    else:
        return JsonResponse({'message': 'error'}, status=400)


def email_verification(request):
    return render(request, "authapp/email_verification.html", {})


def email_verification_done(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.verified = True
        user.save()
        # login(request, user)
        return render(request, 'authapp/email_verification_complete.html')
    else:
        return render(request, 'authapp/email_verification_error.html')


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'authapp/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('authapp:password_reset_done')
    template_name = 'authapp/password_reset_form.html'
    email_template_name = "authapp/messages/password_reset_email.txt"


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        if (self.request.method == 'POST' and self.request.headers.get(
                'x-requested-with') == 'XMLHttpRequest'):
            data = {'message': 'success'}
            form.save()
            update_session_auth_hash(self.request, form.user)
            return JsonResponse(data, status=200)

    def form_invalid(self, form):
        if (self.request.method == 'POST' and self.request.headers.get(
                'x-requested-with') == 'XMLHttpRequest'):
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
