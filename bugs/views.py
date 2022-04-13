from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.http import Http404, HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from constants.constants import *
from userprofile.views import get_designation, is_manager, get_user_profile
from .forms import BugForm, BugStatusForm
from django.views.generic.edit import FormMixin

from django.contrib.auth.models import User
from userprofile.models import Profile
from project.models import Project
from .models import Bug

from django.views.generic.detail import DetailView
from django.views.generic import ListView


@login_required
@transaction.atomic
def add_bug(request, id, type):
    if not (is_manager(request.user) or get_user_profile(request.user).designation == QAENGINEER):
        raise HttpResponseForbidden()

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
        raise HttpResponseForbidden()

    context = {}

    bug = get_object_or_404(Bug, pk=pk)
    if is_manager(request.user):
        context['manager'] = True
    else:
        if bug.creator.user != request.user:
            raise HttpResponseForbidden

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


@login_required
def delete_bug(request, pk):

    if not is_manager(request.user):
        raise HttpResponseForbidden()
    bug = get_object_or_404(Bug, pk=pk)
    try:
        bug.delete()
    except:  # ProtectedError was not working so I have just used except
        return render(request, "delete_bug.html",  {'title': 'Deletion Failed',
                                                    'msg': "Bug/Feature deletion could not be completed. This should not happen."})
    messages.success(request, "Bug Removed!")
    return redirect('list-bug')


def assign_bug(request, bug_id, user_id):
    user_profile = get_user_profile(request.user)
    desgination = user_profile.designation
    if request.user.id != user_id or desgination != DEVELOPER:
        raise HttpResponseForbidden

    bug = get_object_or_404(Bug, uuid=bug_id)
    if not bug.assigned_to:
        bug.assigned_to = user_profile
        bug.save()
    else:
        raise HttpResponseForbidden
    return redirect('detail-bug', pk=bug.uuid)


class DetailBug(LoginRequiredMixin, FormMixin, DetailView):

    redirect_field_name = 'rt'
    template_name = 'view_bug.html'
    context_object_name = 'bug'
    allow_empty = False
    queryset = Bug.objects.all()
    form_class = BugStatusForm

    def get_success_url(self):
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        return reverse('detail-bug', kwargs={'pk': bug.uuid})

    def get_form_kwargs(self):
        kwargs = super(DetailBug, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def post(self, request, *args, **kwargs):
        profile_user = get_user_profile(self.request.user)
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if profile_user.designation not in (MANAGER, QAENGINEER, DEVELOPER):
            return HttpResponseForbidden()
        if profile_user.designation == DEVELOPER and bug.assigned_to != profile_user:
            return HttpResponseForbidden()

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Status Changed Sucessfully")
            return self.form_valid(form)
        else:
            messages.error(request, "Status Change Failed")
            return self.form_invalid(form)

    def form_valid(self, form):
        status = form.cleaned_data['status']
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        bug.status = status
        bug.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetailBug, self).get_context_data(**kwargs)
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        context['status_form'] = self.get_form
        user_profile = get_user_profile(self.request.user)
        desgination = user_profile.designation
        context['user__type'] = get_designation(user_profile)
        if bug.type == BUG:
            context['bug__status'] = dict(BUG_STATUS).get(bug.status)
        else:
            context['bug__status'] = dict(FEATURE_STATUS).get(bug.status)

        if desgination == MANAGER:
            context['moderator'] = True
        elif user_profile == bug.creator:
            context['creator'] = True
        elif desgination in DEVELOPER:
            context['developer'] = True
            if user_profile == bug.assigned_to:
                context['cuser'] = True

        return context

    def get_object(self):
        current_user = get_user_profile(self.request.user)
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if current_user.designation in (MANAGER, QAENGINEER) or current_user.project == bug.project:
            return bug
        else:
            raise HttpResponseForbidden


class ListBug(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Project
    template_name = 'list_bug.html'
    context_object_name = 'bugs'

    def get_context_data(self, **kwargs):
        context = super(ListBug, self).get_context_data(**kwargs)
        user_profile = get_user_profile(self.request.user)
        context['user__type'] = get_designation(user_profile)
        context['status_list'] = BUG_STATUS
        context['list_title'] = "Manage Bug/Features"
        if 'slug' in self.kwargs:
            if FEATURE == self.kwargs['slug']:
                context['list_title'] = "Manage Features"
                context['statuses'] = FEATURE_STATUS
                context['b_type'] = FEATURE
            elif BUG == self.kwargs['slug']:
                context['list_title'] = "Manage Bugs"
                context['b_type'] = BUG
            elif self.kwargs['slug'] not in (NEW, INPROGRESS, COMPLETED):
                raise Http404

        return context

    def get_queryset(self):
        current_user = get_user_profile(self.request.user)
        if current_user.designation in (QAENGINEER, MANAGER):

            bug_list = Bug.objects.all()
            if 'slug' in self.kwargs:
                if self.kwargs['slug'] in (FEATURE, BUG):
                    if FEATURE == self.kwargs['slug']:
                        bug_list = Bug.objects.filter(type=FEATURE)
                    elif BUG == self.kwargs['slug']:
                        bug_list = Bug.objects.filter(type=BUG)
                elif self.kwargs['slug'] in (NEW, INPROGRESS, COMPLETED):
                    if self.kwargs['slug'] == NEW:
                        bug_list = bug_list.filter(status=NEW)
                    elif self.kwargs['slug'] == INPROGRESS:
                        bug_list = bug_list.filter(status=INPROGRESS)
                    elif self.kwargs['slug'] == COMPLETED:
                        bug_list = bug_list.filter(status=COMPLETED)
                else:
                    raise Http404

            if 'filter' not in self.kwargs:
                return bug_list
            elif self.kwargs['filter'] == NEW:
                return bug_list.filter(status=NEW)
            elif self.kwargs['filter'] == INPROGRESS:
                return bug_list.filter(status=INPROGRESS)
            elif self.kwargs['filter'] == COMPLETED:
                return bug_list.filter(status=COMPLETED)
            else:
                raise Http404
        else:
            raise Http404
