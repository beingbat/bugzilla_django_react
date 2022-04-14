from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin


from django.views.generic.detail import DetailView
from utilities.constants import *

from project.forms.project_chose import *
from project.forms.project_form import *
from project.models.project import *

from userprofile.models.profile import Profile
from bugs.models import Bug

from utilities.user_utils import get_user_profile, get_designation


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
        features = bugs.filter(type=FEATURE)
        bugs = bugs.filter(type=BUG)
        if bugs.count()>0:
            context['bugs'] =  bugs
        if features.count() > 0:
            context['features'] = features
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
            raise PermissionDenied()
