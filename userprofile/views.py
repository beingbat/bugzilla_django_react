from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from userprofile.models import Profile
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
import userprofile.forms as profileforms
from django.contrib import messages

from django.views.generic.edit import FormMixin
from project.forms import ProjectChooseForm
from project.models import Project

from django.http import HttpResponseForbidden
from django.urls import reverse


def index_page(request):
  context = {}
  if(request.user.is_authenticated):
    profileobj = Profile.objects.get(pk=request.user)
    profile = profileobj.designation
    if profileobj.project:
      context["project_name"] = profileobj.project.name
      context["project_id"] = profileobj.project.id
    context["user_type"] = profile
  context["user"] = request.user
  return render(request, 'index.html', context)

#Tried merging add_user and update_user but it created a lot of conditional statements so left it as it is

@login_required
@transaction.atomic
def add_user(request):

  current_user = get_object_or_404(Profile, user=request.user)
  if current_user.designation == 'man':

    if request.method == 'POST':

      user_form = profileforms.UserRegisterForm(request.POST)
      profile_form = profileforms.ProfileForm(request.POST)

      if user_form.is_valid() and profile_form.is_valid():
          user = user_form.save()
          profile = profile_form.save(commit=False)
          profile.user = user
          profile.save()
          messages.success(request, "New Employee has been created successfully")
          return redirect('dashboard')

      else:
          messages.error(request, "Failed adding new employee")

    else: #GET

        user_form = profileforms.UserRegisterForm(request.POST)
        profile_form = profileforms.ProfileForm(request.POST)

    return render(request, "user_add.html", {'user_form': user_form, 'profile_form': profile_form})

  else:
    raise Http404



@login_required
@transaction.atomic
def update_user(request, id):

  current_user = get_object_or_404(Profile, user=request.user)

  if current_user.designation == 'man':

    user = get_object_or_404(User, id=id)
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
      user_form = profileforms.UserUpdateForm(request.POST, instance=user)
      profile_form = profileforms.ProfileForm(request.POST, instance=profile)

      if user_form.is_valid() and profile_form.is_valid():

        user = user_form.save()
        profile_form.save()
        messages.success(request, "Employee Information has been updated successfully.")
        return redirect('user-detail', pk=user.id)

      else:
          messages.error(request, "Updating Employee Information Failed.")

    else: #GET


      user_form = profileforms.UserUpdateForm(instance = user)
      profile_form = profileforms.ProfileForm(instance = profile)

    return render(request, "user_update.html", {'user_form': user_form, 'profile_form': profile_form})

  else:
    raise Http404


@login_required
def delete_user(request, id):
  try:

    current_user = get_object_or_404(Profile, user=request.user)
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
    if chosen_project != '-1':
      my_profile = get_object_or_404(Profile, user=get_object_or_404(User, pk=self.kwargs['pk']))
      my_project = my_profile.project
      my_project = get_object_or_404(Project, id=chosen_project)
      my_profile.project = my_project
      my_profile.save()

    return super().form_valid(form)

  def get_context_data(self, **kwargs):
    context = super(UserDetailView, self).get_context_data(**kwargs)
    context["project_form"] = self.get_form
    my_profile = get_object_or_404(Profile, user=get_object_or_404(User, pk=self.kwargs['pk']))
    my_project = my_profile.project
    if my_project:
      context['current_project'] = my_project

    return context

  def get_object(self):

    try:
      if not self.request.user.is_authenticated:
        raise Http404
      current_user = get_object_or_404(Profile, user=self.request.user)
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
      current_user = get_object_or_404(Profile, user=self.request.user)
      if current_user.designation == 'man':
        return Profile.objects.filter(designation=self.kwargs['slug'])
      else:
        raise Http404
    except:
      raise Http404
