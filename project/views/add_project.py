from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from utilities.constants import *

from project.forms.project_chose import *
from project.forms.project_form import *
from project.models.project import *

from utilities.user_utils import is_manager, get_user_profile, get_designation


@login_required
@transaction.atomic
def add_project(request):

    if not is_manager(request.user):
        raise PermissionDenied()

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
        raise PermissionDenied()
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
