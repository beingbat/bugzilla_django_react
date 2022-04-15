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

from django.contrib.auth.models import User


class UserDelete(LoginRequiredMixin, DeleteView):
    queryset = User.objects.all()
    template_name = 'delete_confirmation.html'
    context_object_name = 'object'
    success_url = reverse_lazy('dashboard')
    redirect_field_name = 'rt'
    allow_empty = False

    def get_object(self):
        user = get_object_or_404(User, id=self.kwargs['id'])
        if not is_manager(self.request.user):
            messages.error(
                self.request, f"You don't have permission to delete Employee: {user.username}!")
            raise PermissionDenied()
        return user

    def get_context_data(self, **kwargs):
        context = super(UserDelete, self).get_context_data(**kwargs)
        user_profile = get_user_profile(self.request.user)
        context['user__type'] = get_designation(user_profile)
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
        except:
            messages.error(request, 'User Deletion Failed!')
            return HttpResponseRedirect(success_url)
        messages.success(
            request, f"User: '{self.object.username}' removed")
        return HttpResponseRedirect(success_url)
