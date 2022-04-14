from django.shortcuts import render, redirect, get_object_or_404

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from utilities.constants import *
from utilities.user_utils import is_manager


from bugs.models.bug import Bug


@login_required
def delete_bug(request, pk):

    if not is_manager(request.user):
        raise PermissionDenied()
    bug = get_object_or_404(Bug, pk=pk)
    try:
        bug.delete()
    except:  # ProtectedError was not working so I have just used except
        return render(request, "delete_bug.html",  {'title': 'Deletion Failed',
                                                    'msg': "Bug/Feature deletion could not be completed. This should not happen."})
    messages.success(request, "Bug Removed!")
    return redirect('list-bug')
