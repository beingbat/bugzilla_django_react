from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse_lazy, reverse

from django.core.exceptions import PermissionDenied
from django.db.models import ProtectedError

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utilities.constants import *
from utilities.user_utils import is_manager


from bugs.models.bug import Bug
from django.views.generic.edit import DeleteView

from utilities.user_utils import *

class BugDelete(DeleteView):
    redirect_field_name = 'rt'
    template_name = 'delete_confirmation.html'
    queryset = Bug.objects.all()
    context_object_name = 'object'
    allow_empty = False
    success_url = reverse_lazy('list-bug')

    def get_object(self):
        bug = get_object_or_404(Bug, uuid=self.kwargs['pk'])
        if not is_manager(self.request.user):
            messages.error(self.request, f"You don't have permission to delete {bug.type}: {bug.title}!")
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
        except ProtectedError:
            messages.error(request, 'Deletion Failed! Can not Delete the bug!')
            return HttpResponseRedirect(success_url)
        messages.success(request, f"{self.object.type} '{self.object.title}' removed")
        return HttpResponseRedirect(success_url)

# @login_required
# def delete_bug(request, pk):

#     if not is_manager(request.user):
#         raise PermissionDenied()
#     bug = get_object_or_404(Bug, pk=pk)
#     try:
#         bug.delete()
#     except:  # ProtectedError was not working so I have just used except
#         return render(request, "delete_bug.html",  {'title': 'Deletion Failed',
#                                                     'msg': "Bug/Feature deletion could not be completed. This should not happen."})
#     messages.success(request, "Bug Removed!")
#     return redirect('list-bug')
