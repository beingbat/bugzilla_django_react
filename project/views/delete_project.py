from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from utilities.constants import *
from utilities.user_utils import *

from django.views.generic.edit import DeleteView

from project.forms.project_chose import *
from project.forms.project_form import *
from project.models.project import *

class ProjectDelete(LoginRequiredMixin, DeleteView):
    queryset = Project.objects.all()
    template_name = "delete_confirmation.html"
    context_object_name = 'object'
    success_url = reverse_lazy('list-project')
    redirect_field_name = 'rt'
    allow_empty = False

    def get_object(self):
        project = get_object_or_404(Project, pk=self.kwargs['id'])
        if not is_manager(self.request.user):
            messages.error(
                self.request, f"You don't have permission to delete {project.title}!")
            raise PermissionDenied()
        return project

    def get_context_data(self, **kwargs):
        context = super(ProjectDelete, self).get_context_data(**kwargs)
        user_profile = get_user_profile(self.request.user)
        context['user__type'] = get_designation(user_profile)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except:
            messages.error(request, 'Project Deletion Failed. Please remove all employees from project first!')
            return HttpResponseRedirect(success_url)
        messages.success(
            request, f"Project '{self.object.title}' removed")
        return HttpResponseRedirect(success_url)
