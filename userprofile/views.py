from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import Http404
from django.http import HttpResponseForbidden, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.views.generic.edit import FormMixin
from project.forms import ProjectChooseForm
import userprofile.forms as profileforms

from django.contrib.auth.models import User
from userprofile.models import Profile
from project.models import Project

from constants import constants
from bugs.models import Bug
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.contrib.auth import login, authenticate


def get_designation(profile):
    if profile.designation == constants.MANAGER:
        return 'Manager'
    else:
        return dict(constants.USER_TYPES).get(profile.designation)


def is_manager(user):
    current_user = get_object_or_404(Profile, user=user)
    return True if current_user.designation == constants.MANAGER else False


def get_user_profile(user):
    return get_object_or_404(Profile, user=user)


def get_user_profile_by_id(user_id):
    user = get_object_or_404(User, id=user_id)
    return get_object_or_404(Profile, user=user)


def page_not_found(request, exception):

    return render(request, "errors/404.html", {})


def index_page(request):
    context = {}
    if(request.user.is_authenticated):
        profileobj = Profile.objects.get(pk=request.user)
        profile = profileobj.designation

        if profileobj.project:
            context["project_name"] = profileobj.project.name
            context["project_id"] = profileobj.project.id
        context["user_type"] = profile
        context["user__type"] = get_designation(profileobj)
        context['user_profile'] = profileobj

    context["user"] = request.user
    context["types"] = constants.USER_TYPES
    context["manager"] = constants.MANAGER
    if Profile.objects.filter(designation=constants.DEVELOPER).count() > 0:
        context['dev_list'] = True
    if Profile.objects.filter(designation=constants.QAENGINEER).count() > 0:
        context['qae_list'] = True

    if Bug.objects.all().count() > 0:
        context['bugs'] = True
    return render(request, 'index.html', context)

# Tried merging add_user and update_user but it created a lot of conditional statements so left it as it is


@login_required
@transaction.atomic
def add_user(request):

    if not is_manager(request.user):
        raise Http404

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


@login_required
@transaction.atomic
def update_user(request, id):

    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)
    man = is_manager(request.user)
    if not (is_manager(request.user) or profile.user == request.user):
        raise Http404

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


@login_required
def delete_user(request, id):
    if not is_manager(request.user):
        raise Http404

    u = User.objects.get(id=id)
    try:
        u.delete()
    except:
        return HttpResponse("Deleting User Failed!")
    messages.success(request, "The user is deleted")

    return redirect(index_page)


class UserDetailView(LoginRequiredMixin, FormMixin, DetailView):

    redirect_field_name = 'rt'
    template_name = 'profile_view.html'
    context_object_name = 'user_profile'
    allow_empty = False
    queryset = Profile.objects.all()
    form_class = ProjectChooseForm

    def get_success_url(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return reverse('user-detail', kwargs={'pk': user.pk})

    def get_form_kwargs(self):
        kwargs = super(UserDetailView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def post(self, request, *args, **kwargs):
        if not is_manager(request.user):
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        chosen_project = form.cleaned_data['projects_field']
        if chosen_project != '-1':
            my_profile = get_user_profile_by_id(self.kwargs['pk'])
            my_project = my_profile.project
            my_project = get_object_or_404(Project, id=chosen_project)
            my_profile.project = my_project
            my_profile.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["project_form"] = self.get_form
        my_profile = get_user_profile_by_id(self.kwargs['pk'])
        my_project = my_profile.project
        if my_project:
            context['current_project'] = my_project
        context['type'] = my_profile.designation
        context["user__type"] = get_designation(
            get_object_or_404(Profile, user=self.request.user))
        if get_object_or_404(Profile, user=self.request.user).designation == constants.MANAGER:
            context['moderator'] = True
        return context

    def get_object(self):
        profile_to_view = get_user_profile_by_id(self.kwargs['pk'])
        if is_manager(self.request.user) or profile_to_view.user == self.request.user:
            return profile_to_view
        raise Http404


class UserListView(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'user_list'
    allow_empty = False

    def get_queryset(self):
        if not is_manager(self.request.user):
            raise Http404
        return Profile.objects.filter(designation=self.kwargs['slug'])

    def get_context_data(self, **kwargs):

        if not is_manager(self.request.user):
            raise Http404
        context = super(UserListView, self).get_context_data(**kwargs)
        my_profile = get_user_profile_by_id(self.request.user.id)
        context['type'] = my_profile.designation
        if self.kwargs['slug'] == constants.DEVELOPER:
            context['list_title'] = "Manage Developers"
        elif self.kwargs['slug'] == constants.QAENGINEER:
            context['list_title'] = "Manage QAEngineers"
        context['user__type'] = get_designation(my_profile)
        return context
