
from django.shortcuts import render, redirect

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User

from utilities.user_utils import *

import views.index_page as index_page

@login_required
def delete_user(request, id):
    if not is_manager(request.user):
        raise PermissionDenied()

    u = User.objects.get(id=id)
    try:
        u.delete()
    except:
        return render(request, "errors/generic.html",
                    {'title':'User deletion failed because it is linked to a bug or feature. Remove its link to delete it.'})
    messages.success(request, "The user is deleted")

    return redirect(index_page)
