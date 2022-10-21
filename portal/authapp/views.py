from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, \
    LoginView
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView

from portal.settings import SITE_DOMAIN, SITE_PROTOCOL
from .forms import UserRegistrationForm, CustomPasswordChangeForm, \
    CustomPasswordResetForm, UserLoginForm

User = get_user_model()

account_activation_token = default_token_generator


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('authapp:email_verification')
    template_name = 'authapp/signup.html'

    def form_valid(self, form):
        super(SignUpView, self).form_valid(form)
        user = User.objects.get(email=form.cleaned_data['email'])
        mail_subject = 'Activate your blog account.'
        message = render_to_string(
            'authapp/messages/email_verification_message.txt', {
                'user': user,
                'domain': SITE_DOMAIN,
                'protocol': SITE_PROTOCOL,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponseRedirect(self.get_success_url())


def email_verification(request):
    return render(request, "authapp/email_verification.html", {})


def email_verification_done(request, uidb64, token):
    print(uidb64)
    print(token)
    print(request.scheme)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
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


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm

    def form_valid(self, form):
        if (self.request.method == 'POST' and self.request.headers.get(
                'x-requested-with') == 'XMLHttpRequest'):
            print(111111111111)
            data = {'message': 'success'}
            form.save()
            update_session_auth_hash(self.request, form.user)
            return JsonResponse(data, status=200)

    def form_invalid(self, form):
        if (self.request.method == 'POST' and self.request.headers.get(
                'x-requested-with') == 'XMLHttpRequest'):
            errors = form.errors
            return JsonResponse({"errors": errors}, status=400)
