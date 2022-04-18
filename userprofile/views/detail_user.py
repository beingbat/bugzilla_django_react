from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.views.generic.detail import DetailView

from django.views.generic.edit import FormMixin
from project.forms import ProjectChooseForm

from django.contrib.auth.models import User
from userprofile.models import Profile
from project.models import Project

from utilities import *


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
            return PermissionDenied()

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Project Changed Successfully!")
            return self.form_valid(form)
        else:
            messages.error(request, "Project Change Failed")
            return self.form_invalid(form)

    def form_valid(self, form):
        chosen_project = form.cleaned_data['projects_field']
        my_profile = get_user_profile_by_id(self.kwargs['pk'])
        if chosen_project != '-1':
            my_project = get_object_or_404(Project, id=chosen_project)
            my_profile.project = my_project
            my_profile.save()
        else:
            my_profile.project = None
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
        if get_object_or_404(Profile, user=self.request.user).designation == MANAGER:
            context['moderator'] = True
        return context

    def get_object(self):
        profile_to_view = get_user_profile_by_id(self.kwargs['pk'])
        if is_manager(self.request.user) or profile_to_view.user == self.request.user:
            return profile_to_view
        raise PermissionDenied()
