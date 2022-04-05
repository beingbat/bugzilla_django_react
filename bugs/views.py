from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from userprofile.views import is_manager, get_user_profile
from constants.constants import *
from django.contrib import messages
from .forms import BugForm
from .models import Bug
from django.contrib.auth.models import User
from project.models import Project
from userprofile.models import Profile

from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
@transaction.atomic
def add_bug(request, id):
    if not (is_manager(request.user) or get_user_profile(request.user).designation == QAENGINEER):
        raise Http404

    context = {}

    if is_manager(request.user):
        context['manager'] = True

    if request.method == 'POST':
        bug_form = BugForm(request.POST, project_id=id)
        project = get_object_or_404(Project, id=id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            bug.project = project
            bug.status = NEW
            bug.creator = get_user_profile(request.user)
            dev_id = bug_form.cleaned_data.get("assigned_dev")

            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.save()
            messages.success(request, "Bug created sucessfully")
            return redirect('detail-bug', pk=bug.uuid)
        else:
            messages.error(request, "Error occured in Bug creation")
    else:  # GET
        bug_form = BugForm(request.POST, project_id=id)

    context['bug_form'] = bug_form
    return render(request, 'add_bug.html', context)


@login_required
@transaction.atomic
def update_bug(request, pk):
    if not (is_manager(request.user) or get_user_profile(request.user).designation == QAENGINEER):
        raise Http404

    context = {}

    if is_manager(request.user):
        context['manager'] = True

    bug = get_object_or_404(Bug, pk=pk)
    if request.method == 'POST':
        bug_form = BugForm(request.POST, instance=bug, project_id=bug.project.id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            dev_id = bug_form.cleaned_data.get("assigned_dev")

            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.save()
            messages.success(request, "Bug Updated Successfully")
            return redirect('detail-bug', bug.uuid)
        else:
            messages.error(request, "Bug Updation Failed")
    else:
        bug_form = BugForm(instance=bug, project_id=bug.project.id)

    context['bug_form'] = bug_form
    return render(request, 'update_bug.html', context)


@login_required
def delete_bug(request, pk):

    if not is_manager(request.user):
        raise Http404
    bug = get_object_or_404(Bug, pk=pk)
    try:
        bug.delete()
    except:  # ProtectedError was not working so I have just used except
        return render(request, "delete_bug.html",  {'title': 'Deletion Failed',
                                                    'msg': "Deletion Failed. Bug can't be deleted."})
    messages.success(request, "Bug Removed!")
    return redirect('list-bug')


class DetailBug(LoginRequiredMixin, DetailView):

    redirect_field_name = 'rt'
    template_name = 'view_bug.html'
    context_object_name = 'bug'
    allow_empty = False
    queryset = Bug.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetailBug, self).get_context_data(**kwargs)
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if get_user_profile(self.request.user).designation in (MANAGER, QAENGINEER):
            context['moderator'] = True

        return context

    def get_object(self):
        current_user = get_user_profile(self.request.user)
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if is_manager(self.request.user) or current_user.designation == QAENGINEER or (current_user.project and current_user.project == bug.project):
            return bug
        else:
            raise Http404


class ListBug(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Project
    template_name = 'list_bug.html'
    context_object_name = 'bugs'

    def get_queryset(self):
        current_user = get_user_profile(self.request.user)
        if is_manager(self.request.user) or current_user.designation == QAENGINEER:
            return Bug.objects.all()
        else:
            raise Http404
