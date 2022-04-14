from django.shortcuts import render, get_object_or_404, redirect

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import transaction

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from userprofile.tokens import account_activation_token

from userprofile.models.profile import Profile
from django.contrib.auth.models import User

import userprofile.forms as profileforms

from utilities.user_utils import *


@login_required
@transaction.atomic
def add_user(request):

    if not is_manager(request.user):
        raise PermissionDenied()

    if request.method == 'POST':

        user_form = profileforms.UserRegisterForm(request.POST)
        profile_form = profileforms.ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.is_active = False
            user.save()
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your bugzilla account.'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(
                request, "New Employee has been created successfully")
            return render(request, "confirmation_page.html", {})

        else:
            messages.error(request, "Failed adding new employee")

    else:  # GET

        user_form = profileforms.UserRegisterForm()
        profile_form = profileforms.ProfileForm()

    profile = get_object_or_404(Profile, user=request.user)
    context = {'form_title': "please enter new employee information",
               'button_text': "Add Employee", 'user_form': user_form,
               'profile_form': profile_form
               }
    context["user__type"] = get_designation(profile)
    context['moderator'] = True
    context['user'] = request.user
    return render(request, "user_add.html", context)


@login_required
@transaction.atomic
def update_user(request, id):

    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)
    man = is_manager(request.user)
    if not (is_manager(request.user) or profile.user == request.user):
        raise PermissionDenied()

    if request.method == 'POST':
        user_form = profileforms.UserUpdateForm(request.POST, instance=user)
        valid = True
        if man:
            profile_form = profileforms.ProfileForm(
                request.POST, instance=profile)
            valid = profile_form.is_valid()

        if user_form.is_valid() and valid:
            user = user_form.save()
            if man:
                profile_form.save()
            messages.success(
                request, "Employee Information has been updated successfully.")
            return redirect('user-detail', pk=user.id)

        else:
            messages.error(request, "Updating Employee Information Failed.")

    else:  # GET

        user_form = profileforms.UserUpdateForm(instance=user)
        profile_form = profileforms.ProfileForm(instance=profile)
    context = {'form_title': "please update employee information",
               'button_text': "Update Employee", 'user_form': user_form, 'profile_form': profile_form}
    context["user__type"] = get_designation(profile)
    context['user'] = request.user
    if is_manager(request.user):
        context['moderator'] = True
    return render(request, "user_add.html", context=context)
