from django.shortcuts import render, get_object_or_404, redirect

from django.core.exceptions import PermissionDenied

from django.contrib import messages


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from userprofile.tokens import account_activation_token

from userprofile.models.profile_model import Profile
from django.contrib.auth.models import User

from userprofile.forms import *

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


from utilities import *


class CreateUserProfile(LoginRequiredMixin, CreateView):
    model = Profile
    fields = "__all__"
    template_name = "add_user.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        self.current_user = get_object_or_404(Profile, user=self.request.user)
        if self.current_user.designation != MANAGER:
            raise PermissionDenied()
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
        context["profile_form"] = profile_form
        context["user_form"] = user_form
        return render(request, "user_add.html", context)

    def post(self, request, *args, **kwargs):
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.is_active = False
            user.save()
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your bugzilla account."
            message = render_to_string(
                "activate_account.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = user_form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            messages.success(request, "New Employee has been created successfully")
            return render(request, "confirmation_page.html")

        context = self.get_context_data()
        context["user_form"] = user_form
        context["profile_form"] = profile_form
        messages.error(request, "Failed adding new employee")
        return render(request, "user_add.html", context)

    def get_context_data(self, **kwargs):
        context = super(CreateUserProfile, self).get_context_data(**kwargs)
        context["form_title"] = "please enter new employee information"
        context["button_text"] = "Add Employee"
        context["user"] = self.request.user
        context["moderator"] = True
        context["user__type"] = self.current_user.designation
        return context


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = "__all__"

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        self.current_user = get_object_or_404(Profile, user=self.request.user)
        if self.current_user.designation != MANAGER:
            raise PermissionDenied()

        self.update_user = get_object_or_404(User, id=kwargs["id"])
        self.update_profile = get_object_or_404(Profile, user=self.update_user)
        return super(UpdateUserProfile, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        user_form = UserUpdateForm(instance=self.update_user)
        profile_form = ProfileForm(instance=self.update_profile)
        context["profile_form"] = profile_form
        context["user_form"] = user_form
        return render(request, "user_add.html", context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        user_form = UserUpdateForm(request.POST, instance=self.update_user)
        valid = True
        profile_form = ProfileForm(request.POST, instance=self.update_profile)
        valid = profile_form.is_valid()

        if user_form.is_valid() and valid:
            user = user_form.save()
            profile_form.save()
            messages.success(
                request, "Employee Information has been updated successfully."
            )
            return redirect("user-detail", pk=user.id)

        messages.error(request, "Updating Employee Information Failed.")
        return render(request, "user_add.html", context=context)

    def get_context_data(self, **kwargs):
        context = super(UpdateUserProfile, self).get_context_data(**kwargs)
        context["form_title"] = "please update employee information"
        context["button_text"] = "Update Employee"
        context["user"] = self.request.user
        context["moderator"] = True
        context["user__type"] = self.current_user.designation
        return context
