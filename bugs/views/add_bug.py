from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from constants.constants import *
from utilities.user_utils import get_designation, is_manager, get_user_profile
from bugs.forms.bug_form import BugForm

from django.contrib.auth.models import User
from userprofile.models.profile import Profile
from project.models.project import Project
from bugs.models.bug import Bug


@login_required
@transaction.atomic
def add_bug(request, id, type):
    if not (is_manager(request.user) or get_user_profile(request.user).designation == QAENGINEER):
        raise PermissionDenied()

    if type not in ('bug', 'feature'):
        raise Http404
    elif type == 'bug':
        entity_type = BUG
    elif type == 'feature':
        entity_type = FEATURE

    context = {}
    if is_manager(request.user):
        context['manager'] = True
    if request.method == 'POST':
        bug_form = BugForm(request.POST, request.FILES, count_allowed=0, project_id=id)
        project = get_object_or_404(Project, id=id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            bug.project = project
            bug.status = NEW
            bug.creator = get_user_profile(request.user)
            bug.type = entity_type
            dev_id = bug_form.cleaned_data.get("assigned_dev")

            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.save()
            messages.success(request, "Bug/Feature created sucessfully")
            return redirect('detail-bug', pk=bug.uuid)
        else:
            messages.error(request, "Error occured in Bug creation")
    else:  # GET
        bug_form = BugForm(count_allowed=0, project_id=id)

    context['bug_form'] = bug_form
    context['user__type'] = get_designation(get_user_profile(request.user))
    if entity_type == BUG:
        context['form_title'] = "Please add bug information below"
        context['button_text'] = "Add Bug"
    elif entity_type == FEATURE:
        context['form_title'] = "Please add feature information below"
        context['button_text'] = "Add Feature"

    return render(request, 'add_bug.html', context)


@login_required
@transaction.atomic
def update_bug(request, pk):
    designation = get_user_profile(request.user).designation
    if designation not in (MANAGER, QAENGINEER):
        raise PermissionDenied()

    context = {}

    bug = get_object_or_404(Bug, pk=pk)
    if is_manager(request.user):
        context['manager'] = True
    else:
        if bug.creator.user != request.user:
            raise PermissionDenied()

    if request.method == 'POST':
        bug_form = BugForm(request.POST, request.FILES, instance=bug,
                            count_allowed=1, project_id=bug.project.id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            dev_id = bug_form.cleaned_data.get("assigned_dev")

            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.screenshot = bug_form.cleaned_data.get("screenshot")
            bug.save()
            messages.success(request, "Bug Updated Successfully")
            return redirect('detail-bug', bug.uuid)
        else:
            messages.error(request, "Bug Updation Failed")
    else:
        bug_form = BugForm(instance=bug, count_allowed=1, project_id=bug.project.id)

    context['bug_form'] = bug_form
    context['user__type'] = get_designation(get_user_profile(request.user))
    if bug.type == BUG:
        context['form_title'] = "Please update bug information below"
        context['button_text'] = "Update Bug"
    elif bug.type == FEATURE:
        context['form_title'] = "Please update feature information below"
        context['button_text'] = "Update Feature"

    return render(request, 'add_bug.html', context)

