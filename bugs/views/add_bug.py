from django.shortcuts import render, redirect, get_object_or_404

from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.contrib import messages

from constants.constants import *
from bugs.forms.bug_form import BugForm

from django.contrib.auth.models import User
from userprofile.models.profile import Profile
from project.models.project import Project
from bugs.models.bug import Bug

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

import logging


class CreateBug(LoginRequiredMixin, CreateView):
    model = Bug
    fields = '__all__'
    template_name = "add_bug.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        self.profile = get_object_or_404(Profile, user=request.user)
        if self.profile.designation not in (QAENGINEER, MANAGER):
            raise PermissionDenied()
        self.project_id = kwargs['pk']
        if kwargs['slug'] not in (BUG, FEATURE):
            raise Http404
        self.bug_type = kwargs['slug']
        return super(CreateBug, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        logging.debug(kwargs)
        context['bug_form'] = BugForm(
            count_allowed=0, project_id=self.project_id)
        return render(request, 'add_bug.html', context)

    def post(self, request, *args, **kwargs):
        bug_form = BugForm(request.POST, request.FILES,
                           count_allowed=0, project_id=self.project_id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            bug.project = get_object_or_404(Project, id=self.project_id)
            bug.status = NEW
            bug.creator = self.profile
            bug.type = self.bug_type
            dev_id = bug_form.cleaned_data.get("assigned_dev")

            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.save()
            messages.success(request, "Bug/Feature created sucessfully")
            return redirect('detail-bug', pk=bug.uuid)
        messages.error(request, "Error occured in Bug creation")
        context = self.get_context_data()
        context['bug_form'] = bug_form
        return render(request, 'add_bug.html', context)

    def get_context_data(self, **kwargs):
        context = super(CreateBug, self).get_context_data(**kwargs)
        context['user__type'] = self.profile.designation
        if self.bug_type == BUG:
            context['form_title'] = "Please add bug information below"
            context['button_text'] = "Add Bug"
        elif self.bug_type == FEATURE:
            context['form_title'] = "Please add feature information below"
            context['button_text'] = "Add Feature"
        return context


class UpdateBug(LoginRequiredMixin, UpdateView):
    model = Bug
    fields = ['title', 'description', 'deadline', 'assigned_to', 'screenshot']
    success_message = 'Updated Successfully'
    template_name = "add_bug.html"
    context_object_name = 'bug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        context['bug_form'] = BugForm(
            instance=self.object, count_allowed=1, project_id=self.object.project.id)
        return render(request, 'add_bug.html', context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        bug_form = BugForm(request.POST, request.FILES, instance=self.object,
                           count_allowed=1, project_id=self.object.project.id)
        if bug_form.is_valid():
            bug = bug_form.save(commit=False)
            dev_id = bug_form.cleaned_data.get("assigned_dev")
            if bug_form.cleaned_data.get("assigned_dev") != '-1':
                bug.assigned_to = get_object_or_404(
                    Profile, user=get_object_or_404(User, id=dev_id))

            bug.save()
            messages.success(request, "Bug/Feature updated sucessfully")
            return redirect('detail-bug', pk=bug.uuid)
        messages.error(request, "Error occured in Bug updation")
        context = self.get_context_data()
        context['bug_form'] = bug_form
        return render(request, 'add_bug.html', context)

    def get_context_data(self, **kwargs):
        context = super(UpdateBug, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        context['user__type'] = profile.designation
        if context['bug'].type == BUG:
            context['form_title'] = "Please update bug information below"
            context['button_text'] = "Update Bug"
        elif context['bug'].type == FEATURE:
            context['form_title'] = "Please add feature information below"
            context['button_text'] = "Update Feature"
        return context
