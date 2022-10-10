from django.contrib.auth import get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView

from .forms import UserRegistrationForm, CustomPasswordChangeForm, \
    CustomPasswordResetForm

User = get_user_model()

account_activation_token = default_token_generator


class SignUpView(CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main:main')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        super(SignUpView, self).form_valid(form)
        user = User.objects.get(email=form.cleaned_data['email'])
        mail_subject = 'Activate your blog account.'
        message = render_to_string(
            'users/messages/email_verification_message.txt', {
                'user': user,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponseRedirect(self.get_success_url())


def verify_email(request, uidb64, token):
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
        user.save()
        login(request, user)
        return render(request, 'users/email_verification_complete.html')
    else:
        return render(request, 'users/email_verification_error.html')


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    template_name = 'users/password_change_form.html'


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('users:password_reset_done')
    template_name = 'users/password_reset_form.html'
