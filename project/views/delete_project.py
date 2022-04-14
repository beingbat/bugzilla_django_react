from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from utilities.constants import *

from project.forms.project_chose import *
from project.forms.project_form import *
from project.models.project import *

from utilities.user_utils import is_manager



@login_required
def delete_project(request, id):

    if not is_manager(request.user):
        raise PermissionDenied()
    project = Project.objects.get(id=id)
    try:
        project.delete()
    except:  # ProtectedError was not working so I have just used except
        return render(request, "delete_project.html", {'title': 'Project Deletion Failed',
                                                       'msg': "Project has employees linked to it, please remove them first to delete it."})
    messages.success(request, "Project Removed!")
    return redirect('list-project')
