from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseForbidden

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import ProtectedError

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from constants.constants import *

from .forms import *

from .models import *
from userprofile.models import Profile
from bugs.models import Bug

from userprofile.views import is_manager, get_user_profile, get_designation


@login_required
@transaction.atomic
def add_project(request):

    if not is_manager(request.user):
        raise HttpResponseForbidden()

    if request.method == 'POST':
        project_form = ProjectForm(request.POST)

        if project_form.is_valid():
            project = project_form.save()
            messages.success(request, "Project Created Successfully")
            return redirect('detail-project', project.id)
        else:
            messages.error(request, "Project Creation Failed.")
    else:
        project_form = ProjectForm()
    designation = get_designation(
        get_user_profile(request.user))
    context = {'form_title': "Please add project information below",
               'project_form': project_form, 'button_text': "Add Project",
               'user__type': designation}
    return render(request, "add_project.html", context)


@login_required
@transaction.atomic
def update_project(request, id):

    if not is_manager(request.user):
        raise HttpResponseForbidden()
    project = get_object_or_404(Project, id=id)
    if request.method == 'POST':
        project_form = ProjectForm(request.POST, instance=project)
        if project_form.is_valid():
            project_form.save()
            messages.success(request, "Project Updated Successfully")
            return redirect('detail-project', project.id)
        else:
            messages.error(request, "Project Updation Failed")
    else:
        project_form = ProjectForm(instance=project)
    designation = get_designation(
        get_user_profile(request.user))
    context = {'form_title': "Please update project information below",
               'project_form': project_form, 'button_text': "Update Project",
               'user__type': designation}
    return render(request, "add_project.html", context)


@login_required
def delete_project(request, id):

    if not is_manager(request.user):
        raise HttpResponseForbidden()
    project = Project.objects.get(id=id)
    try:
        project.delete()
    except:  # ProtectedError was not working so I have just used except
        return render(request, "delete_project.html", {'title': 'Project Deletion Failed',
                                                       'msg': "Project has employees linked to it, please remove them first to delete it."})
    messages.success(request, "Project Removed!")
    return redirect('list-project')


class DetailProject(LoginRequiredMixin, DetailView):

    redirect_field_name = 'rt'
    template_name = 'view_project.html'
    context_object_name = 'project'
    allow_empty = False
    queryset = Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailProject, self).get_context_data(**kwargs)

        current_user = get_user_profile(self.request.user)
        context['designation'] = current_user.designation
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        employees = Profile.objects.filter(project=project)
        qaes = employees.filter(designation=QAENGINEER)
        devs = employees.filter(designation=DEVELOPER)
        bugs = Bug.objects.filter(project=project)
        context['bugs'] = bugs
        context['qaes'] = qaes
        context['devs'] = devs
        context['qaengineer'] = QAENGINEER
        context['developer'] = DEVELOPER
        context['manager'] = MANAGER
        context['user__type'] = get_designation(current_user)
        return context

    def get_object(self):
        current_user = get_user_profile(self.request.user)
        if current_user.designation in (QAENGINEER, MANAGER) or (current_user.project and current_user.project.id == self.kwargs['pk']):
            return Project.objects.get(id=self.kwargs['pk'])
        else:
            raise HttpResponseForbidden()


class ListProjects(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Project
    template_name = 'list_projects.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        current_user = get_user_profile(self.request.user)
        if current_user.designation in (QAENGINEER, MANAGER):
            return Project.objects.all()
        else:
            raise HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        context = super(ListProjects, self).get_context_data(**kwargs)
        context['list_title'] = "Manage projects"
        context['user__type'] = get_designation(
            get_user_profile(self.request.user))
        return context
