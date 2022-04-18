from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from utilities.constants import *

from project.forms.project_chose import *
from project.forms.project_form import *
from project.models.project import *

from utilities.user_utils import get_user_profile, get_designation


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
            raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(ListProjects, self).get_context_data(**kwargs)
        context['list_title'] = "Manage projects"
        context['user__type'] = get_designation(
            get_user_profile(self.request.user))
        return context
