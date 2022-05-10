from django.shortcuts import render

from userprofile.models import Profile
from bugs.models import Bug


from utilities import *


def index_page(request):
    context = {}
    if request.user.is_authenticated:
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
                    context["bugs_assigned"] = bugs
                if features.count() > 0:
                    context["features_assigned"] = features

        if profile == QAENGINEER:
            bugs = Bug.objects.filter(creator=profileobj)
            features = bugs.filter(type=FEATURE)
            bugs = bugs.filter(type=BUG)
            if bugs.count() > 0:
                context["bugs_created"] = bugs
            if features.count() > 0:
                context["features_created"] = features

        context["user_type"] = profile
        context["user__type"] = get_designation(profileobj)
        context["user_profile"] = profileobj

    context["user"] = request.user
    context["types"] = USER_TYPES
    context["manager"] = MANAGER
    if Profile.objects.filter(designation=DEVELOPER).count() > 0:
        context["dev_list"] = True
    if Profile.objects.filter(designation=QAENGINEER).count() > 0:
        context["qae_list"] = True

    if Bug.objects.all().count() > 0:
        context["bugs"] = True
    return render(request, "index_dashboard.html", context)
