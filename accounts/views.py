from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str

from .forms import RegisterForm


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            token = default_token_generator.make_token(user)

            verification_url = request.build_absolute_uri(
                reverse(
                    'accounts:verify_email',
                    kwargs={
                        'uidb64': uid,
                        'token': token
                    }
                )
            )

            print(
                'EMAIL VERIFICATION LINK:',
                verification_url
            )

            return render(
                request,
                'accounts/registration_success.html',
                {
                    'verification_url': verification_url
                }
            )

    else:
        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


def verify_email(request, uidb64, token):
    try:
        uid = force_str(
            urlsafe_base64_decode(uidb64)
        )

        user = User.objects.get(pk=uid)

    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()

        return render(
            request,
            'accounts/email_verified.html'
        )

    return render(
        request,
        'accounts/email_verification_failed.html'
    )