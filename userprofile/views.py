from http.client import HTTPResponse
from operator import index
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from userprofile.models import Profile
from django.http import Http404, HttpResponse as hr
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import userprofile.forms as ff
from django.contrib import messages

from django.views.generic.edit import FormMixin
from project.forms import ProjectChooseForm
from project.models import Project

from django.http import HttpResponseForbidden
from django.urls import reverse


def index_page(request):
  if(request.user.is_authenticated):
    profile = Profile.objects.get(pk=request.user).designation
  else:
    profile = ""

  print(type(profile), ": ", profile, "\n")

  context = {
    "user": request.user,
    "user_type": profile,
    }

  return render(request, 'index.html', context)

@login_required
@transaction.atomic
def add_user(request):
    try:
      current_user = Profile.objects.get(user=request.user)
      if current_user.designation == 'man':
        if request.method == 'POST':
              user_form = ff.UserRegisterForm(request.POST)
              profile_form = ff.ProfileForm(request.POST)
              if user_form.is_valid() and profile_form.is_valid():
                  user = user_form.save()
                  profile = profile_form.save()
                  profile.user = user
                  profile.save()
                  messages.success(request, f'Account has been created! You can now log in.')
                  return redirect('dashboard')
              else:
                  messages.error(request, f'Please correct the errors.')
        else:
            user_form = ff.UserRegisterForm(request.POST)
            profile_form = ff.ProfileForm(request.POST)
        return render(request, "user_add.html", {'user_form': user_form, 'profile_form': profile_form})
      else:
        raise Http404
    except:
      raise Http404



@login_required
@transaction.atomic
def update_user(request, id):
    # try:
      current_user = Profile.objects.get(user=request.user)
      if current_user.designation == 'man':
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)
        if request.method == 'POST':
          user_form = ff.UserUpdateForm(request.POST, instance=user)
          profile_form = ff.ProfileForm(request.POST, instance=profile)
          if user_form.is_valid() and profile_form.is_valid():
              # user.username = user_form.cleaned_data['username']
              # user.first_name = user_form.cleaned_data['last_name']
              # user.last_name = user_form.cleaned_data['first_name']
              # profile.designation = profile_form.cleaned_data['designation']
              # user.save()
              # profile.save()
              user_form.save()
              profile_form.save()
              messages.success(request, f'Account has been created! You can now log in.')
              return redirect('user-detail', user.id)
          else:
              messages.error(request, f'Please correct the errors.')
        else:
          user_form = ff.UserUpdateForm(instance = user)
          profile_form = ff.ProfileForm(instance= profile)
        return render(request, "user_update.html", {'user_form': user_form, 'profile_form': profile_form})
      else:
        raise Http404
    # except:
    #   raise Http404


@login_required
def delete_user(request, id):
    try:
      current_user = Profile.objects.get(user=request.user)
      if current_user.designation == 'man':
        u = User.objects.get(id = id)
        u.delete()
        messages.success(request, "The user is deleted")
      else:
        raise Http404
    except:
      raise Http404

    return redirect(index_page)


class UserDetailView(LoginRequiredMixin, FormMixin, DetailView):

  redirect_field_name = 'rt'

  template_name = 'profile_view.html'
  context_object_name = 'user_profile'
  allow_empty = False
  queryset = Profile.objects.all()
  form_class = ProjectChooseForm


  def get_success_url(self):
    user=get_object_or_404(User, pk=self.kwargs['pk'])
    return reverse('user-detail', kwargs={'pk': user.pk})

  def post(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
          return HttpResponseForbidden()
      self.object = self.get_object()
      form = self.get_form()
      if form.is_valid():
          return self.form_valid(form)
      else:
          return self.form_invalid(form)

  def form_valid(self, form):

    chosen_project = form.cleaned_data['projects_field']
    print("Chosing: ", chosen_project)
    if chosen_project != '-1':
      my_profile = get_object_or_404(Profile, user=get_object_or_404(User, pk=self.kwargs['pk']))
      my_project = my_profile.project
      # if not my_project:
      my_project = get_object_or_404(Project, id=chosen_project)
      my_profile.project = my_project
      my_profile.save()

    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(UserDetailView, self).get_context_data(**kwargs)
    context["project_form"] = self.get_form
    projects = Project.objects.all()
    my_profile = get_object_or_404(Profile, user=get_object_or_404(User, pk=self.kwargs['pk']))
    my_project = my_profile.project
    # if projects:
    #   context['projects'] = projects
    if my_project:
      context['current_project'] = my_project

    return context

  def get_object(self):

    try:
      if not self.request.user.is_authenticated:
        raise Http404

      current_user = Profile.objects.get(user=self.request.user)
      if current_user.designation == 'man':
        return Profile.objects.get(user=User.objects.get(id=self.kwargs['pk']))
      else:
        raise Http404
    except:
      raise Http404



class UserListView(LoginRequiredMixin, ListView):

  redirect_field_name = 'rt'
  model = Profile

  template_name = 'profile_list.html'
  context_object_name = 'user_list'
  allow_empty = False

  def get_queryset(self):
        try:
          current_user = Profile.objects.get(user=self.request.user)
          if current_user.designation == 'man':
            return Profile.objects.filter(designation=self.kwargs['slug'])
          else:
            raise Http404
        except:
          raise Http404
