from django.shortcuts import redirect, get_object_or_404

from django.core.exceptions import PermissionDenied

from utilities import *

from bugs.models import Bug


def assign_bug(request, bug_id, user_id):
    user_profile = get_user_profile(request.user)
    desgination = user_profile.designation
    if request.user.id != user_id or desgination != DEVELOPER:
        raise PermissionDenied()

    bug = get_object_or_404(Bug, uuid=bug_id)
    if not bug.assigned_to:
        bug.assigned_to = user_profile
        bug.save()
    else:
        raise PermissionDenied()
    return redirect('detail-bug', pk=bug.uuid)
