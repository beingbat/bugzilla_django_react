from django.shortcuts import render, get_object_or_404, redirect

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db import transaction

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from userprofile.tokens import account_activation_token

from userprofile.models.profile import Profile
from bugs.models.bug import Bug


from utilities.user_utils import *

from utilities.constants import *


def index_page(request):
    context = {}
    if(request.user.is_authenticated):
        profileobj = Profile.objects.get(pk=request.user)
        profile = profileobj.designation

        if profileobj.project:
            context["project_name"] = profileobj.project.name
            context["project_id"] = profileobj.project.id
            if profile == DEVELOPER:
                bugs = Bug.objects.filter(assigned_to=profileobj)
                features = bugs.filter(type=FEATURE)
                bugs = bugs.filter(type=BUG)
                if bugs.count() > 0:
                    context['bugs_assigned'] = bugs
                if features.count() > 0:
                    context['features_assigned'] = features

            elif profile == QAENGINEER:
                bugs = Bug.objects.filter(creator=profileobj)
                features = bugs.filter(type=FEATURE)
                bugs = bugs.filter(type=BUG)
                if bugs.count() > 0:
                    context['bugs_created'] = bugs
                if features.count() > 0:
                    context['features_created'] = features

        context["user_type"] = profile
        context["user__type"] = get_designation(profileobj)
        context['user_profile'] = profileobj

    context["user"] = request.user
    context["types"] = USER_TYPES
    context["manager"] = MANAGER
    if Profile.objects.filter(designation=DEVELOPER).count() > 0:
        context['dev_list'] = True
    if Profile.objects.filter(designation=QAENGINEER).count() > 0:
        context['qae_list'] = True

    if Bug.objects.all().count() > 0:
        context['bugs'] = True
    return render(request, 'index.html', context)
