from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied

from django.contrib import messages

from utilities.constants import *

from project.forms import *
from project.models import Project
from userprofile.models import Profile

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CreateProject(LoginRequiredMixin, CreateView):
    model = Project
    fields = "__all__"
    template_name = "add_project.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = None
        self.profile = get_object_or_404(Profile, user=self.request.user)
        if self.profile.designation != MANAGER:
            raise PermissionDenied()
        return super(CreateProject, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["form"] = ProjectForm()
        return render(request, "add_project.html", context)

    def post(self, request, *args, **kwargs):
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project = project_form.save()
            project.save()
            print("Project id: ", project.id)
            messages.success(request, "Project Created Successfully")
            return redirect("detail-project", pk=project.pk)
        else:
            # print(project_form.errors)
            pass

        messages.error(request, "Project Creation Failed.")
        context = self.get_context_data()
        context["form"] = project_form
        return render(request, "add_project.html", context)

    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        context["user__type"] = self.profile.designation
        context["button_text"] = "Add Project"
        context["form_title"] = "Please add project information below"
        return context


class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    fields = "__all__"
    success_message = "Updated Project Successfully"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        context["form"] = ProjectForm(instance=self.object)
        return render(request, "add_project.html", context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        project_form = ProjectForm(request.POST, instance=self.object)

        if project_form.is_valid():
            project = project_form.save()
            messages.success(request, "Project Created Successfully")
            return redirect("detail-project", project.id)

        messages.error(request, "Error occured in Project updation")
        context = self.get_context_data()
        context["form"] = project_form
        return render(request, "add_project.html", context)

    def get_context_data(self, **kwargs):
        context = super(UpdateProject, self).get_context_data(**kwargs)
        profile = get_object_or_404(Profile, user=self.request.user)
        context["user__type"] = profile.designation
        context["button_text"] = "Update Project"
        context["form_title"] = "Please update project information below"

        return context
