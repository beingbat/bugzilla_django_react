from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView

from userprofile.models import Profile

from utilities import *


class UserListView(LoginRequiredMixin, ListView):

    redirect_field_name = 'rt'
    model = Profile
    template_name = 'profile_list.html'
    context_object_name = 'user_list'
    allow_empty = False

    def get_queryset(self):
        if not is_manager(self.request.user):
            raise PermissionDenied()
        return Profile.objects.filter(designation=self.kwargs['slug'])

    def get_context_data(self, **kwargs):

        if not is_manager(self.request.user):
            raise Http404
        context = super(UserListView, self).get_context_data(**kwargs)
        my_profile = get_user_profile_by_id(self.request.user.id)
        context['type'] = my_profile.designation
        if self.kwargs['slug'] == DEVELOPER:
            context['list_title'] = "Manage Developers"
        elif self.kwargs['slug'] == QAENGINEER:
            context['list_title'] = "Manage QAEngineers"
        context['user__type'] = get_designation(my_profile)
        return context
