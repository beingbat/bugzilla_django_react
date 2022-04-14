from django.http import Http404

from django.contrib.auth.mixins import LoginRequiredMixin

from constants.constants import *
from utilities.user_utils import get_designation, get_user_profile

from project.models.project import Project
from bugs.models.bug import Bug

from django.views.generic import ListView


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

            if 'filter' not in self.kwargs or self.kwargs['filter'] == ALL:
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
