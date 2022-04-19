from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from utilities import *
from bugs.forms import BugStatusForm
from django.views.generic.edit import FormMixin

from bugs.models.bug_model import Bug

from django.views.generic.detail import DetailView


class DetailBug(LoginRequiredMixin, FormMixin, DetailView):

    redirect_field_name = "rt"
    template_name = "view_bug.html"
    context_object_name = "bug"
    allow_empty = False
    queryset = Bug.objects.all()
    form_class = BugStatusForm

    def get_success_url(self):
        bug = get_object_or_404(Bug, uuid=self.kwargs["pk"])
        return reverse("detail-bug", kwargs={"pk": bug.uuid})

    def get_form_kwargs(self):
        kwargs = super(DetailBug, self).get_form_kwargs()
        kwargs["pk"] = self.kwargs["pk"]
        return kwargs

    def post(self, request, *args, **kwargs):
        profile_user = get_user_profile(self.request.user)
        bug = get_object_or_404(Bug, uuid=self.kwargs["pk"])
        if profile_user.designation not in (MANAGER, QAENGINEER, DEVELOPER):
            return PermissionDenied()
        if profile_user.designation == DEVELOPER and bug.assigned_to != profile_user:
            return PermissionDenied()

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            messages.success(request, "Status Changed Sucessfully")
            return self.form_valid(form)
        else:
            messages.error(request, "Status Change Failed")
            return self.form_invalid(form)

    def form_valid(self, form):
        status = form.cleaned_data["status"]
        bug = get_object_or_404(Bug, uuid=self.kwargs["pk"])
        bug.status = status
        bug.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DetailBug, self).get_context_data(**kwargs)
        bug = get_object_or_404(Bug, uuid=self.kwargs["pk"])
        context["status_form"] = self.get_form
        user_profile = get_user_profile(self.request.user)
        desgination = user_profile.designation
        context["user__type"] = get_designation(user_profile)
        if bug.type == BUG:
            context["bug__status"] = dict(BUG_STATUS).get(bug.status)
        else:
            context["bug__status"] = dict(FEATURE_STATUS).get(bug.status)

        if desgination == MANAGER:
            context["moderator"] = True
        elif user_profile == bug.creator:
            context["creator"] = True
        elif desgination in DEVELOPER:
            context["developer"] = True
            if user_profile == bug.assigned_to:
                context["cuser"] = True

        return context

    def get_object(self):
        current_user = get_user_profile(self.request.user)
        bug = get_object_or_404(Bug, uuid=self.kwargs["pk"])
        if (
            current_user.designation in (MANAGER, QAENGINEER)
            or current_user.project == bug.project
        ):
            return bug
        else:
            raise PermissionDenied()
