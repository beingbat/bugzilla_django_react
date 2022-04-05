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


def is_manager(user):
    current_user = get_object_or_404(Profile, user=user)
    return True if current_user.designation == constants.MANAGER else False


def get_user_profile(user):
    return get_object_or_404(Profile, user=user)


def get_user_profile_by_id(user_id):
    user = get_object_or_404(User, id=user_id)
    return get_object_or_404(Profile, user=user)


def index_page(request):
    context = {}
    if(request.user.is_authenticated):
        profileobj = Profile.objects.get(pk=request.user)
        profile = profileobj.designation

        if profileobj.project:
            context["project_name"] = profileobj.project.name
            context["project_id"] = profileobj.project.id

        context["user_type"] = profile
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
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(
                request, "New Employee has been created successfully")
            return redirect('dashboard')

        else:
            messages.error(request, "Failed adding new employee")

    else:  # GET

        user_form = profileforms.UserRegisterForm(request.POST)
        profile_form = profileforms.ProfileForm(request.POST)

    return render(request, "user_add.html", {'user_form': user_form, 'profile_form': profile_form})


@login_required
@transaction.atomic
def update_user(request, id):

    if not is_manager(request.user):
        raise Http404

    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        user_form = profileforms.UserUpdateForm(request.POST, instance=user)
        profile_form = profileforms.ProfileForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            profile_form.save()
            messages.success(
                request, "Employee Information has been updated successfully.")
            return redirect('user-detail', pk=user.id)

        else:
            messages.error(request, "Updating Employee Information Failed.")

    else:  # GET

        user_form = profileforms.UserUpdateForm(instance=user)
        profile_form = profileforms.ProfileForm(instance=profile)

    return render(request, "user_update.html", {'user_form': user_form, 'profile_form': profile_form})


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
        return context

    def get_object(self):
        if not is_manager(self.request.user):
            raise Http404
        return get_user_profile_by_id(self.kwargs['pk'])


class UserListView(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'user_list'
    allow_empty = False

    def get_queryset(self):
        if not is_manager(self.request.user):
            return HttpResponseForbidden()
        return Profile.objects.filter(designation=self.kwargs['slug'])
