from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages

from utilities import *

from bugs.models import Bug

from django.views.generic.edit import DeleteView


class BugDelete(LoginRequiredMixin, DeleteView):
    queryset = Bug.objects.all()
    template_name = 'delete_confirmation.html'
    context_object_name = 'object'
    success_url = reverse_lazy('list-bug')
    redirect_field_name = 'rt'
    allow_empty = False

    def get_object(self):
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if not (is_manager(self.request.user) or self.request.user==bug.creator):
            messages.error(
                self.request, f"You don't have permission to delete {bug.type}: {bug.title}!")
            raise PermissionDenied()
        return bug

    def get_context_data(self, **kwargs):
        context = super(BugDelete, self).get_context_data(**kwargs)
        user_profile = get_user_profile(self.request.user)
        context['user__type'] = get_designation(user_profile)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except:
            messages.error(request, 'Deletion Failed! Can not Delete the bug!')
            return HttpResponseRedirect(success_url)
        messages.success(
            request, f"{self.object.type} '{self.object.title}' removed")
        return HttpResponseRedirect(success_url)
