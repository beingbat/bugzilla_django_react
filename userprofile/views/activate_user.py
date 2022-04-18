from django.shortcuts import redirect

from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text

from userprofile.tokens import account_activation_token

from django.contrib.auth import login
from django.contrib.auth.models import User


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid!')

